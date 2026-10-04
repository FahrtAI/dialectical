import { resolve } from "node:path";

import { authConfigFromEnvironment } from "./auth.js";
import { createApp } from "./app.js";
import { DialecticalStore } from "./store.js";

const port = Number.parseInt(process.env.DIALECTICAL_PORT ?? "8787", 10);
const host = process.env.DIALECTICAL_HOST ?? "127.0.0.1";
const dbPath = resolve(process.env.DIALECTICAL_DB_PATH ?? "./data/dialectical.sqlite");

if (!Number.isInteger(port) || port < 1 || port > 65535) {
  throw new Error("DIALECTICAL_PORT must be an integer from 1 to 65535");
}

const store = new DialecticalStore(dbPath);
const service = createApp({ store, auth: authConfigFromEnvironment(), host });
const httpServer = service.app.listen(port, host, () => {
  console.log(`Dialectical MCP listening at http://${host}:${port}/mcp`);
});

async function shutdown(): Promise<void> {
  await service.close(httpServer);
  store.close();
}

process.once("SIGINT", () => void shutdown());
process.once("SIGTERM", () => void shutdown());
