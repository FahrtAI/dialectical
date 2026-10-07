# Skills-only architecture audit — 0.4.0

## Finding

The previous package bundled a conversation methodology with an optional
persistence service, then incorrectly required that service for installation.
No method in the core conversation needs proprietary computation, an external
database, credentials, or a continuously running process.

The audit covered all first-party source, manifests, skill instructions and
references, QA/eval cases, packaging scripts, adapters, artwork metadata, and
the server dependency/build layout before modification. Installed dependency
code and generated server output are build artifacts, not methodology.

## Inventory and disposition

| Component before cleanup | Purpose | Disposition |
|---|---|---|
| Root plugin.json | Portable identity and OpenAI listing | Retained; version 0.4.0; honest skills-only capabilities |
| .codex-plugin/plugin.json | Duplicate compatibility manifest | Removed; inline OpenAI extension already exists |
| mcp.json and .mcp.json | Localhost connection declarations | Removed |
| server/src/app.ts and index.ts | HTTP/MCP listener, sessions, startup | Removed |
| server/src/auth.ts | OAuth/JWT verification and development identity | Removed |
| server/src/store.ts | SQLite inquiry/memory database, history, versioning | Removed |
| server/src/tools.ts | Ten persistence/profile MCP tools | Removed |
| server/test/ | Protocol, authentication and storage tests | Removed with the service |
| Server package/lock, TypeScript, Docker and environment files | Service dependencies, build and deployment | Removed |
| 20 skills and supporting Markdown | Actual operations, router, examples, trust boundaries | Retained; startup and no-storage continuity made explicit |
| Memory reference | MCP mapping plus file format | MCP mapping removed; optional existing file format preserved |
| ASCII help card | Stable orientation text | Retained; persistence promises corrected |
| QA/cases/mcp.yaml | Service integration expectations | Replaced by server-free ChatGPT cases |
| Other QA and evals | Methodology, routing and optional host tests | Retained; capability requirements distinguished |
| Package scripts | ZIP assembly and validation | Simplified; no compulsory MCP or hosting checks |
| README, CHATGPT.md and other adapters | Product and installation instructions | Corrected; other hosts remain optional |
| assets/ | README banners and plugin icons | Retained; only referenced plugin icons are shipped |
| dist/ | Built ZIP with localhost connection | Rebuilt as a skills-only distribution |

Tracked removals remain recoverable from Git history. Ignored generated server
files and the superseded ZIP were moved outside the repository during cleanup.
No user inquiry store was removed.

## Minimum package versus preserved methodology

OpenAI's portable package example needs a root manifest and a
skills/<name>/SKILL.md entry. Skills use name and description YAML frontmatter.
The OpenAI interface extension gives this package the display name Dialectical.
An MCP declaration is optional and is absent here.

The existing focused operations have distinct triggers and success criteria;
retaining them avoids rewriting the methodology as one large prompt. References
are loaded only when needed. No compatibility overlay or runtime wrapper is
required for the current portable format.

## Acceptance boundary

The entry skill explicitly handles “@Dialectical start a conversation” in the
current chat. Without a supplied topic it asks what to explore. Storage and
worker capabilities are optional. Research still needs actual evidence to make
research claims; without access it reports the limit.

Local structural validation is separate from OpenAI upload checks, account
installation, and observed desktop/iPhone behavior. See [CHATGPT.md](../CHATGPT.md)
and [the device cases](../QA/cases/chatgpt.yaml). Do not report those device tests
as passed merely because the ZIP is valid.

## Current sources

- [Portable package structure and optional compatibility overlay](https://developers.openai.com/plugins/build/plugins)
- [Skills may operate without MCP](https://developers.openai.com/plugins/concepts/skills)
- [Skill frontmatter, resources and workflow boundaries](https://developers.openai.com/plugins/build/skills)
- [Metadata limits; policy URLs and tool review requirements are MCP-specific](https://developers.openai.com/plugins/deploy/submission)
- [Account creation/editing and @ invocation](https://learn.chatgpt.com/docs/build-plugins)
- [Desktop/mobile support and installation](https://learn.chatgpt.com/docs/plugins)

The build-skills page includes a legacy manifest illustration. For this package
the dedicated portable packaging specification governs: discover skills/ by
convention, with presentation under extensions.com.openai, not top-level skills
or apps fields.
