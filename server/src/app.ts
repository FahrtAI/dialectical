import { randomUUID } from "node:crypto";
import type { Server } from "node:http";

import { createMcpExpressApp } from "@modelcontextprotocol/sdk/server/express.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { isInitializeRequest } from "@modelcontextprotocol/sdk/types.js";
import type { Request, Response } from "express";

import {
  AuthenticationError,
  READ_SCOPE,
  WRITE_SCOPE,
  type AuthConfig,
  type AuthContext,
  createAuthenticator,
  resourceMetadataUrl,
} from "./auth.js";
import { DialecticalStore } from "./store.js";
import { createDialecticalMcpServer } from "./tools.js";

interface Session {
  transport: StreamableHTTPServerTransport;
  auth: AuthContext;
  lastActive: number;
}

export interface AppOptions {
  store: DialecticalStore;
  auth: AuthConfig;
  host?: string;
  maxSessions?: number;
  sessionIdleMs?: number;
}

function rpcError(response: Response, status: number, code: number, message: string): void {
  response.status(status).json({ jsonrpc: "2.0", error: { code, message }, id: null });
}

export function createApp(options: AppOptions) {
  const host = options.host ?? "127.0.0.1";
  const app = createMcpExpressApp({ host });
  const authenticate = createAuthenticator(options.auth);
  const sessions = new Map<string, Session>();
  const maxSessions = options.maxSessions ?? 1000;
  const sessionIdleMs = options.sessionIdleMs ?? 30 * 60_000;
  const metadataUrl = resourceMetadataUrl(options.auth);

  app.get("/health", (_request, response) => {
    response.json({ status: "ok", service: "dialectical-memory", version: "0.3.0" });
  });

  app.get("/.well-known/oauth-protected-resource", (_request, response) => {
    if (options.auth.mode !== "oauth" || !options.auth.resourceUrl || !options.auth.issuer) {
      response.status(404).json({ error: "oauth_not_configured" });
      return;
    }
    response.json({
      resource: options.auth.resourceUrl,
      authorization_servers: [options.auth.issuer],
      scopes_supported: [READ_SCOPE, WRITE_SCOPE],
      ...(options.auth.documentationUrl
        ? { resource_documentation: options.auth.documentationUrl }
        : {}),
    });
  });

  async function identity(request: Request, response: Response): Promise<AuthContext | undefined> {
    try {
      return await authenticate(request);
    } catch (error) {
      const message = error instanceof Error ? error.message : "Unauthorized";
      const status = error instanceof AuthenticationError ? 401 : 500;
      if (metadataUrl) {
        response.setHeader(
          "WWW-Authenticate",
          `Bearer resource_metadata="${metadataUrl}", scope="${READ_SCOPE} ${WRITE_SCOPE}"`,
        );
      }
      response.status(status).json({ error: "unauthorized", message });
      return undefined;
    }
  }

  function getSession(request: Request, response: Response, auth: AuthContext): Session | undefined {
    const sessionId = request.header("mcp-session-id");
    if (!sessionId) return undefined;
    const session = sessions.get(sessionId);
    if (!session) {
      rpcError(response, 404, -32001, "Session not found");
      return undefined;
    }
    if (session.auth.userId !== auth.userId) {
      rpcError(response, 403, -32002, "Session belongs to another user");
      return undefined;
    }
    const sameScopes =
      session.auth.scopes.size === auth.scopes.size &&
      [...session.auth.scopes].every((scope) => auth.scopes.has(scope));
    if (!sameScopes) {
      rpcError(response, 403, -32003, "Authorization scopes changed; initialize a new session");
      return undefined;
    }
    session.lastActive = Date.now();
    return session;
  }

  app.post("/mcp", async (request, response) => {
    const auth = await identity(request, response);
    if (!auth) return;
    const suppliedSessionId = request.header("mcp-session-id");
    if (suppliedSessionId) {
      const session = getSession(request, response, auth);
      if (!session) return;
      await session.transport.handleRequest(request, response, request.body);
      return;
    }
    if (!isInitializeRequest(request.body)) {
      rpcError(response, 400, -32000, "Initialization request or valid session ID required");
      return;
    }
    if (sessions.size >= maxSessions) {
      rpcError(response, 503, -32000, "Too many open sessions");
      return;
    }

    let transport: StreamableHTTPServerTransport;
    transport = new StreamableHTTPServerTransport({
      sessionIdGenerator: () => randomUUID(),
      onsessioninitialized: (sessionId) => {
        sessions.set(sessionId, { transport, auth, lastActive: Date.now() });
      },
    });
    transport.onclose = () => {
      if (transport.sessionId) sessions.delete(transport.sessionId);
    };
    const server = createDialecticalMcpServer(options.store, auth, metadataUrl);
    await server.connect(transport);
    await transport.handleRequest(request, response, request.body);
  });

  app.get("/mcp", async (request, response) => {
    const auth = await identity(request, response);
    if (!auth) return;
    const session = getSession(request, response, auth);
    if (!session) {
      if (!response.headersSent) rpcError(response, 400, -32000, "MCP session ID required");
      return;
    }
    await session.transport.handleRequest(request, response);
  });

  app.delete("/mcp", async (request, response) => {
    const auth = await identity(request, response);
    if (!auth) return;
    const session = getSession(request, response, auth);
    if (!session) {
      if (!response.headersSent) rpcError(response, 400, -32000, "MCP session ID required");
      return;
    }
    await session.transport.handleRequest(request, response);
  });

  const reaper = setInterval(() => {
    const cutoff = Date.now() - sessionIdleMs;
    for (const session of sessions.values()) {
      if (session.lastActive < cutoff) void session.transport.close();
    }
  }, Math.min(sessionIdleMs, 60_000));
  reaper.unref();

  return {
    app,
    sessions,
    close: async (httpServer?: Server) => {
      clearInterval(reaper);
      await Promise.all([...sessions.values()].map(({ transport }) => transport.close()));
      await new Promise<void>((resolve, reject) => {
        if (!httpServer) return resolve();
        httpServer.close((error) => (error ? reject(error) : resolve()));
      });
    },
  };
}
