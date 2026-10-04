# Dialectical MCP server

This service supplies durable inquiry and memory tools to the Dialectical
plugin. It uses the MCP streamable HTTP transport and keeps every record scoped
to the authenticated user's subject identifier.

## Local development

Node.js 22.13 or newer is required because the store uses `node:sqlite`.

```sh
cd server
npm install
cp .env.example .env
npm run dev
```

The development authentication mode requires an
`x-dialectical-user-id` header. It exists only for local testing. Production
startup fails unless `DIALECTICAL_AUTH_MODE=oauth`.

Useful commands:

```sh
npm run typecheck
npm test
npm run build
```

The local plugin manifests point to `http://127.0.0.1:8787/mcp`. Update both
`mcp.json` and `.mcp.json` to the deployed HTTPS endpoint before packaging a
production release.

## Authentication

OAuth mode validates JWT access tokens against a remote JWKS and requires:

- `DIALECTICAL_OAUTH_ISSUER`
- `DIALECTICAL_OAUTH_AUDIENCE`
- `DIALECTICAL_OAUTH_JWKS_URL`
- `DIALECTICAL_RESOURCE_URL`

The authorization server must support OAuth 2.1 authorization code with PKCE
and publish its own discovery metadata. This server publishes protected
resource metadata, emits authentication challenges, declares read/write scopes
on every tool, verifies token issuer/audience/time/signature, and enforces
`dialectical:read` or `dialectical:write` in the tool handler. The token `sub`
claim is the storage partition key. A session initialized by one subject cannot
be reused by another. `get_profile` exposes that stable opaque identifier to
help ChatGPT distinguish connected accounts.

## Persistence guarantees

- SQLite transactions protect multi-record lifecycle updates.
- Every mutation increments a record version.
- Callers must pass `expected_version` to update existing records.
- Optional idempotency keys make retried creates and writes safe.
- Status history and audit rows are append-only.
- There is no delete tool in v1.

The SQLite backend is appropriate for local development and a single-instance
deployment with a persistent volume. A horizontally scaled production service
should replace it with a transactional shared database while preserving the
same store contract.

## Production deployment

Build the included container with `server/` as the build context. Configure a
persistent path for `DIALECTICAL_DB_PATH`, put the service behind HTTPS, and
provide OAuth settings through the host's secret manager. The public endpoint
must remain stable and reachable at a path such as `/mcp`.

The repository intentionally does not contain credentials, a production URL,
privacy/terms URLs, or a registered ChatGPT connection ID. Those release
inputs must be supplied by the publisher before public submission.
