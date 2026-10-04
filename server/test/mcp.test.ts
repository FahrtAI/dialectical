import assert from "node:assert/strict";
import type { AddressInfo } from "node:net";
import { test } from "node:test";

import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

import { createApp } from "../src/app.js";
import { DialecticalStore } from "../src/store.js";

test("MCP endpoint advertises and executes the persistence tools", async () => {
  const store = new DialecticalStore(":memory:");
  const service = createApp({ store, auth: { mode: "dev" } });
  const httpServer = service.app.listen(0, "127.0.0.1");
  await new Promise<void>((resolve) => httpServer.once("listening", resolve));
  const { port } = httpServer.address() as AddressInfo;
  const transport = new StreamableHTTPClientTransport(
    new URL(`http://127.0.0.1:${port}/mcp`),
    { requestInit: { headers: { "x-dialectical-user-id": "integration-user" } } },
  );
  const client = new Client({ name: "dialectical-test", version: "0.1.0" });

  try {
    await client.connect(transport);
    const tools = await client.listTools();
    assert.deepEqual(
      tools.tools.map(({ name }) => name).sort(),
      [
        "checkpoint_inquiry",
        "get_inquiry",
        "get_memory_object",
        "get_profile",
        "list_inquiries",
        "save_memory_object",
        "search_memory",
        "set_inquiry_status",
        "start_inquiry",
        "update_memory_metadata",
      ],
    );
    const readTool = tools.tools.find(({ name }) => name === "get_inquiry");
    assert.deepEqual(readTool?._meta?.securitySchemes, [
      { type: "oauth2", scopes: ["dialectical:read"] },
    ]);
    const profile = await client.callTool({ name: "get_profile", arguments: {} });
    assert.equal((profile.structuredContent as { id: string }).id, "integration-user");

    const response = await client.callTool({
      name: "start_inquiry",
      arguments: {
        title: "MCP round trip",
        focus: "Confirm the server can create and retrieve inquiry state.",
        idempotency_key: "round-trip-1",
      },
    });
    assert.equal(response.isError, undefined);
    const created = (response.structuredContent as { result: { id: string } }).result;

    const fetched = await client.callTool({
      name: "get_inquiry",
      arguments: { id: created.id },
    });
    assert.equal(
      (fetched.structuredContent as { result: { title: string } }).result.title,
      "MCP round trip",
    );
  } finally {
    await client.close();
    await service.close(httpServer);
    store.close();
  }
});

test("OAuth metadata is discoverable and unauthenticated initialization is challenged", async () => {
  const store = new DialecticalStore(":memory:");
  const service = createApp({
    store,
    auth: {
      mode: "oauth",
      issuer: "https://identity.example.com/",
      audience: "https://dialectical.example.com",
      jwksUrl: "https://identity.example.com/.well-known/jwks.json",
      resourceUrl: "https://dialectical.example.com",
      documentationUrl: "https://dialectical.example.com/docs",
    },
  });
  const httpServer = service.app.listen(0, "127.0.0.1");
  await new Promise<void>((resolve) => httpServer.once("listening", resolve));
  const { port } = httpServer.address() as AddressInfo;
  try {
    const metadata = await fetch(
      `http://127.0.0.1:${port}/.well-known/oauth-protected-resource`,
    );
    assert.equal(metadata.status, 200);
    assert.deepEqual(await metadata.json(), {
      resource: "https://dialectical.example.com",
      authorization_servers: ["https://identity.example.com/"],
      scopes_supported: ["dialectical:read", "dialectical:write"],
      resource_documentation: "https://dialectical.example.com/docs",
    });

    const response = await fetch(`http://127.0.0.1:${port}/mcp`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        jsonrpc: "2.0",
        id: 1,
        method: "initialize",
        params: {
          protocolVersion: "2025-06-18",
          capabilities: {},
          clientInfo: { name: "unauthenticated-test", version: "0.1.0" },
        },
      }),
    });
    assert.equal(response.status, 401);
    assert.match(
      response.headers.get("www-authenticate") ?? "",
      /oauth-protected-resource/,
    );
  } finally {
    await service.close(httpServer);
    store.close();
  }
});
