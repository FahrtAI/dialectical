import type { Request } from "express";
import { createRemoteJWKSet, jwtVerify } from "jose";

export class AuthenticationError extends Error {}

export interface AuthConfig {
  mode: "dev" | "oauth";
  issuer?: string;
  audience?: string;
  jwksUrl?: string;
  resourceUrl?: string;
  documentationUrl?: string;
}

export interface AuthContext {
  userId: string;
  scopes: Set<string>;
}

export const READ_SCOPE = "dialectical:read";
export const WRITE_SCOPE = "dialectical:write";

function bearerToken(request: Request): string {
  const header = request.header("authorization");
  if (!header?.startsWith("Bearer ")) throw new AuthenticationError("Bearer token required");
  return header.slice("Bearer ".length).trim();
}

export function authConfigFromEnvironment(): AuthConfig {
  const requested = process.env.DIALECTICAL_AUTH_MODE;
  const mode = requested === "oauth" ? "oauth" : "dev";
  if (process.env.NODE_ENV === "production" && mode !== "oauth") {
    throw new Error("DIALECTICAL_AUTH_MODE=oauth is required in production");
  }
  const config: AuthConfig = {
    mode,
    issuer: process.env.DIALECTICAL_OAUTH_ISSUER,
    audience: process.env.DIALECTICAL_OAUTH_AUDIENCE,
    jwksUrl: process.env.DIALECTICAL_OAUTH_JWKS_URL,
    resourceUrl: process.env.DIALECTICAL_RESOURCE_URL,
    documentationUrl: process.env.DIALECTICAL_DOCUMENTATION_URL,
  };
  if (
    mode === "oauth" &&
    (!config.issuer || !config.audience || !config.jwksUrl || !config.resourceUrl)
  ) {
    throw new Error(
      "DIALECTICAL_OAUTH_ISSUER, DIALECTICAL_OAUTH_AUDIENCE, DIALECTICAL_OAUTH_JWKS_URL, and DIALECTICAL_RESOURCE_URL are required",
    );
  }
  return config;
}

export function resourceMetadataUrl(config: AuthConfig): string | undefined {
  return config.resourceUrl
    ? `${config.resourceUrl.replace(/\/$/, "")}/.well-known/oauth-protected-resource`
    : undefined;
}

export function createAuthenticator(config: AuthConfig): (request: Request) => Promise<AuthContext> {
  if (config.mode === "dev") {
    return async (request) => {
      const userId = request.header("x-dialectical-user-id");
      if (!userId) {
        throw new AuthenticationError(
          "x-dialectical-user-id is required when DIALECTICAL_AUTH_MODE=dev",
        );
      }
      return { userId, scopes: new Set([READ_SCOPE, WRITE_SCOPE]) };
    };
  }

  const jwks = createRemoteJWKSet(new URL(config.jwksUrl!));
  return async (request) => {
    try {
      const { payload } = await jwtVerify(bearerToken(request), jwks, {
        issuer: config.issuer,
        audience: config.audience,
      });
      if (!payload.sub) throw new AuthenticationError("Access token has no subject");
      const rawScopes = typeof payload.scope === "string" ? payload.scope.split(/\s+/) : [];
      return { userId: payload.sub, scopes: new Set(rawScopes.filter(Boolean)) };
    } catch (error) {
      if (error instanceof AuthenticationError) throw error;
      throw new AuthenticationError("Access token is invalid or expired");
    }
  };
}
