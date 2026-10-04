# Dialectical for ChatGPT

The repository root is now a portable Agent Plugins package. `plugin.json`
identifies the plugin, `skills/` supplies the operations, and `mcp.json`
connects those operations to the persistence service in `server/`.

For local development:

1. Install and start the server as described in `server/README.md`.
2. Keep the local MCP URL in `mcp.json` and `.mcp.json` aligned with the server.
3. Enable ChatGPT developer mode and register the MCP connection.
4. Install the complete plugin from a local source and run the cases in `QA/`.

Before public submission, deploy the server to a stable HTTPS `/mcp` endpoint,
enable OAuth, replace both local URLs, add publisher policy/support metadata and
review assets, and rerun the release gates. Static instructions alone are not
durable memory; SAVE, RECALL, and lifecycle operations require the MCP tools.

For the monitoring rules to run in ordinary conversation, add the lines from the
README's "Always-on instructions" section to custom instructions or to a
project's instructions.
