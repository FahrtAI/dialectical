# Skills-only architecture audit — current at 0.7.0

This document records the architectural decision that made Dialectical a
skills-only ChatGPT plugin and describes the state of the repository at release
0.7.0. The original audit was performed during the 0.4.0 cleanup. It remains a
historical record of the removed service, but the inventory and acceptance
notes below are kept current so that this document is useful to maintainers.

## Current finding

Dialectical's product is a conversational methodology. Its core behavior needs
no proprietary computation, external API, database, credentials, background
process, or continuously running service. The portable package therefore
contains a root manifest, the entry skill, focused skills, their references,
the license, and referenced plugin artwork.

Optional continuity can use a record supplied in the conversation or an
authorized filesystem. That optional file format is a host capability; it is
not a required plugin service and it does not turn the ChatGPT package into a
database-backed application.

## Inventory and disposition

| Component | Current purpose | Status |
|---|---|---|
| `plugin.json` | Portable identity, metadata, and OpenAI interface listing | Retained; version 0.7.0 |
| `skills/dialectical/SKILL.md` | Entry behavior, ordinary-conversation boundary, routing, and help behavior | Retained |
| 23 focused skills and supporting Markdown | Independent operations, boundaries, examples, and optional continuity procedures | Retained; skill frontmatter is version 0.7.0 |
| `skills/dialectical/references/memory.md` | Optional file-storage contract and no-storage behavior | Retained; storage schema remains separate from release version |
| `assets/` artwork referenced by the manifest | Plugin icon, logos, and project artwork | Retained; only referenced plugin artwork is packaged |
| `LICENSE` | CC BY-NC-SA 4.0 legal terms | Retained |
| `QA/`, `evals/`, and `scripts/` | Maintainer validation, behavioral fixtures, scoring, and ZIP assembly | Retained in the repository; excluded from the plugin ZIP |
| `README.md`, `CHATGPT.md`, and host guides | Product explanation, installation, and host-testing instructions | Retained and aligned to skills-only behavior |
| `docs/cookbook.md` and `docs/flows.md` | Repository documentation and illustrative usage | Retained outside the package |
| `docs/architecture-audit.md` | This architectural record | Retained and updated for 0.7.0 |
| `.codex-plugin/plugin.json` | Duplicate compatibility manifest | Removed during the 0.4.0 cleanup |
| `mcp.json`, `.mcp.json`, and `.app.json` | Localhost or app connection declarations | Removed during the 0.4.0 cleanup |
| `server/src/` | HTTP/MCP listener, auth, SQLite store, and persistence tools | Removed during the 0.4.0 cleanup |
| `server/test/` | Protocol, authentication, and storage tests | Removed with the service |
| Server package files, TypeScript, Docker, and environment files | Service dependencies, build, and deployment | Removed with the service |

The removed service was an implementation path that had been mistaken for a
requirement of the conversational product. Its tracked history remains
recoverable in Git. No user inquiry store was removed as part of the cleanup.

## What changed after the original audit

The skills-only conversion landed in 0.4.0. Release 0.5.0 added the inquiry
framing operations RELEVANCE, COLLECTION GAPS, and INDICATORS. Release 0.6.0
added GUIDE as an on-demand recommendation. Release 0.6.1 tightened consent
and composition boundaries, improved causal and evidence calibration, reduced
duplication in continuity instructions, and added executable QA and onboarding
documentation. Release 0.7.0 renamed SUMMARIZE to RECAP, separated the in-chat
cookbook from generic flows, made GUIDE a ranked three-choice palette, added the
JOIN conversational handle, and made SAVE a portable Markdown handoff. It also
established concise-by-default responses, visible ordinary-language command
cues, and a toolkit-wide calibration rule that preserves evidence-supported
scope and confidence through transformations.

The current catalog has 24 `SKILL.md` files, including the entry skill. The
operations remain independently callable. Ordinary conversation is primary;
there is no mandatory intelligence cycle, automatic operation chain,
background observer, or scheduled monitoring behavior. GUIDE ranks three useful
commands and waits for one selection; MORE displays the complete catalog. JOIN
uses only prior context supplied by the host. SAVE exports user-owned Markdown
without claiming cross-thread memory. COLLECTION GAPS proposes
evidence to seek, RESEARCH seeks available evidence, VERIFY evaluates a
specific empirical claim, and INDICATORS defines developments to watch without
creating monitoring tasks.

## Minimum package

The current package is intentionally small:

```text
plugin.json
LICENSE
skills/
  <skill-name>/SKILL.md
  <skill-name>/references/*.md
assets/<manifest-referenced PNG files>
```

`plugin.json` uses the portable Agent Plugins 1.0 schema and the
`extensions.com.openai.interface` metadata needed for the Dialectical display
identity. The package has no MCP declaration, app dependency, executable
runtime, wrapper application, hosting target, or required account connection.
Repository documentation, QA fixtures, evaluation adapters, and packaging
utilities remain useful to maintainers but are deliberately outside the ZIP.

The entry skill handles `@Dialectical start a conversation` and JOIN in the current
chat. It can begin with only the packaged instructions. SAVE, CHECKPOINT,
RESUME, and related continuity operations explain their limits when no
authorized storage is available; they do not invent persistence or request a
service merely to continue the conversation.

## Validation boundary

The repository's local checks validate the manifest, paths, artwork, skill
frontmatter, package contents, QA definitions, and evaluation harness. The
package builder runs the package and skill validators before creating the
skills-only ZIP. These checks do not establish that an account accepts an
upload, that an installed plugin invokes correctly, or that artwork renders
correctly in every desktop and mobile host. Those are installation and device
acceptance tests documented in [CHATGPT.md](../CHATGPT.md),
[QA/RUNNING.md](../QA/RUNNING.md), and [QA/RELEASE_ACCEPTANCE.md](../QA/RELEASE_ACCEPTANCE.md).

The current version and archive name are read from `plugin.json`; the current
distribution is `dist/dialectical-0.7.0.zip`. `dist/` is generated output and
is not part of the source package definition.

## Current sources

- [Portable package structure and optional compatibility overlay](https://developers.openai.com/plugins/build/plugins)
- [Skills may operate without MCP](https://developers.openai.com/plugins/concepts/skills)
- [Skill frontmatter, resources and workflow boundaries](https://developers.openai.com/plugins/build/skills)
- [Metadata limits; policy URLs and tool review requirements are MCP-specific](https://developers.openai.com/plugins/deploy/submission)
- [Account creation/editing and @ invocation](https://learn.chatgpt.com/docs/build-plugins)
- [Desktop/mobile support and installation](https://learn.chatgpt.com/docs/plugins)

These links preserve the sources used for the packaging decision. The local
validators are implementation checks, not a substitute for OpenAI upload
scans or installed-host behavior.
