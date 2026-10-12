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

## Full review snapshot

This review was run on October 11, 2026 against version 0.7.0 at commit
`d73a790`. It covers the portable package, all bundled skills and references,
the interaction design, repository documentation, packaging code, and the QA
architecture.

The architectural decision remains correct: Dialectical should stay a
skills-only plugin. Current OpenAI documentation explicitly permits skills to
work without an MCP server when the workflow needs only packaged instructions
and resources. Dialectical needs external evidence tools for some RESEARCH and
VERIFY requests, but it does not own those tools and does not need a server to
conduct the conversation. Adding an MCP server would create deployment,
authentication, privacy, and availability costs without improving the core
method.

There is no release-blocking source or package defect in the reviewed tree. The
largest risk is evidence about behavior: the repository has strong static and
harness tests, but no recorded 0.7.0 configured-model run and no installed-host
desktop or iPhone result. The package is well specified; its actual selection
and conversational behavior are not yet demonstrated to the same standard.

### Architecture map

```text
plugin.json
  └─ discovers skills/ at the package root
       ├─ dialectical/                 entry, routing, consent, ordinary chat
       │    └─ references/             help, cookbook, flows, JOIN, modes, memory
       ├─ 16 reasoning/context skills  independently callable operations
       └─ 7 continuity skills          optional state and retrieval operations

Repository only; not shipped in the plugin ZIP
  ├─ QA/ and evals/                    cases, rubrics, fixtures, acceptance
  ├─ scripts/                          validators, evaluator, package builder
  └─ docs/ and host guides             explanation and maintainer guidance
```

The portable archive has 46 files and contains only `plugin.json`, `LICENSE`,
three referenced PNG assets, skill instructions, and skill references. It has
no `mcp.json`, app binding, server, hook, executable runtime, dependency tree,
credential, or database.

## Architectural strengths and costs

| Choice | Advantages | Costs or risks |
|---|---|---|
| Skills-only package | Minimal installation surface; no uptime, authentication, data-retention, or hosting burden; works for ordinary conversation | RESEARCH and VERIFY depend on evidence capabilities supplied by the host; continuity cannot promise automatic cross-chat recall |
| One entry skill plus focused operations | Each operation has a recognizable goal and explicit boundary; users can invoke only the help they want | Twenty-three peer operations create a large discovery surface and several routing confusion sets |
| Ordinary conversation as the default | Preserves the product's central promise and avoids turning every discussion into a framework | The core's monitoring suggestions and command-learning cue can still feel procedural if applied too eagerly |
| Explicit consent and no automatic chains | Prevents a useful method from becoming an unwanted intelligence cycle | Some operations legitimately use neighboring methods internally, so the composition contract is necessarily subtle |
| Evidence-scope and confidence preservation | Directly addresses hallucination, confirmation bias, source dependence, and overclaiming | Cross-cutting instructions are repeated in every skill, increasing prompt maintenance and the chance of drift |
| Optional file continuity | Preserves compatibility for users with an authorized filesystem without imposing a service | Seven continuity skills and a 1,000-word storage reference are a disproportionate part of a ChatGPT-first product whose default host has no plugin-owned store |
| Deterministic packaging and layered QA | Reproducible ZIPs, path checks, version checks, boundary cases, and honest deferred states | Most QA assets are specifications until a model or installed host actually executes them |

## Problem areas and recommendations

### 1. Behavioral proof trails source quality — high priority

The repository defines 207 QA cases, but validation reports that 61 are
deferred and explicitly states that no behavior was executed. The 54 unit tests
verify the runner, package, and textual contracts; they do not show that a model
routes or follows the skills. No `OPENAI_API_KEY` was available during this
review, so the focused 0.7.0 model suite could not be run. Desktop and iPhone
acceptance are also still untested.

**Recommendation:** before calling 0.7.0 accepted, run `QA/cases/release.yaml`
against a named model for at least three repetitions, review the transcripts,
then complete the separate installed-host record on desktop and iPhone. Keep
model-injected regression, installed-host routing, and qualitative comparison
as three distinct claims.

### 2. The evaluation prompt does not emulate skill discovery — high priority

The Dialectical evaluation condition concatenates all 24 `SKILL.md` files plus
six large references into one instruction block. This is useful as a
worst-case instruction-following test, but it is not evidence that ChatGPT
loaded the right skill, and it gives the performer far more context than an
on-demand host normally needs. The runner correctly marks invocation telemetry
as unavailable, but the resulting transcript can still be mistaken for a
routing result.

**Recommendation:** retain the full-injection condition as a stress test, and
add a target-skill condition that injects the core plus only the expected skill
and required references. Continue to reserve actual activation claims for a
host that exposes invocation evidence. Report instruction tokens for both
conditions so the cost of the current catalog is visible.

### 3. The public catalog is cognitively dense — medium priority

The operation boundaries are generally strong, particularly RECAP versus
DISTILL versus TRACE and COLLECTION GAPS versus RESEARCH versus VERIFY.
Nevertheless, 23 operations at one level are difficult to learn. The help card
is complete but reads as a reference manual rather than an entry point. GUIDE,
the cookbook, and flows mitigate this, but they add three more orientation
concepts the user must understand.

**Recommendation:** keep every skill independently callable, but make the
default orientation progressive: show common conversational moves first and
make the full catalog available through MORE. Do not delete specialized skills
until confusion-set tests show whether consolidation would improve routing.

### 4. Continuity is overrepresented relative to the core product — medium priority

SAVE now has a clear, portable Markdown contract and is the best default for
moving between chats. START INQUIRY, CHECKPOINT, RESUME, CLOSE, TAG, and RECALL
still preserve a richer optional filesystem model. That compatibility is
careful and safe, but it expands the catalog and documentation for a capability
that ordinary ChatGPT conversations cannot assume.

**Recommendation:** present SAVE and RESUME as the normal ChatGPT continuity
path. Treat the file-store lifecycle as an advanced compatibility feature in
help and testing. Measure real use before investing further or removing it.

### 5. Delegation advice is portable only as a fallback contract — medium priority

Several analytical skills recommend isolated workers, while also defining a
single-agent fallback. This can reduce anchoring when the host supports it, but
worker availability, context isolation, cost, and invocation traces vary by
surface. The plugin cannot guarantee the architecture merely through Markdown.

**Recommendation:** retain the fallback and test the operation's answer quality
without workers first. Run delegation cases only on a host that exposes enough
trace data to verify what context was shared. Do not describe delegation as a
plugin capability in release claims until observed.

### 6. Cross-cutting policy is repeated in every skill — medium priority

Concision, command cues, calibration, and consent are intentionally reinforced
inside standalone skills because a host may load them independently. That is a
sound portability choice, but changing one rule touches nearly every skill and
the duplicated prose can drift.

**Recommendation:** preserve a short local statement in each skill, but add a
validator-backed canonical checklist for the meaning of the four rules. The
current response-contract tests check for their presence; future checks should
also catch contradictory formulations.

### 7. Packaged and repository-facing examples can drift — medium priority

`docs/cookbook.md` and `docs/flows.md` are richer maintainer-facing documents;
the similarly named packaged references are shorter and optimized for chat.
That difference is intentional, but only headings and selected contracts are
currently synchronized. A conceptual correction can land in one copy without
the other.

**Recommendation:** explicitly designate the repository documents as expanded
sources and the packaged files as chat editions. Add semantic contract tests
for operation names, boundaries, and example conclusions, or generate the chat
editions from marked sections if that remains readable.

### 8. Core behavior contains a controlled product tension — low priority

The entry skill says normal conversation is primary, but it may offer DISTILL
or a check when a conversation becomes hard to hold or begins treating an
untested claim as settled. The constraint to one optional offer is sensible;
nevertheless, this is the only behavior that can introduce method vocabulary
without a direct user request.

**Recommendation:** keep the rule for now, but treat unwanted intervention as a
first-class metric. If ordinary-chat tests show repeated or premature offers,
narrow or remove monitoring rather than adding a background observer.

## Design review

### Product concept

The design has a clear and defensible center: use an LLM to surface connections
and prior art while deliberately protecting against overstatement,
source-blurring, and confirmation bias. “Formalize the interventions, not the
conversation” is the right interaction principle. The strongest design work is
not the number of methods; it is the explicit separation between generating an
idea and establishing it.

### Interaction model

The entry behavior, natural-language routing, and independently callable skills
fit ordinary chat well. GUIDE and JOIN both wait for a choice, which protects
consent. Their menus serve different jobs and should remain separate. The
one-line command cue can teach vocabulary through use, but it should be
evaluated as interface chrome: if it repeatedly makes a simple request feel
formal, the ordinary-conversation promise matters more than command recall.

### Information architecture

The grouping in the README is better than the flat help card because it starts
from user purpose. The catalog should continue moving toward need-first
discovery—understand, explore, test, preserve—while keeping exact operation
names available for experienced users. Cookbook recipes are the most accessible
onboarding surface; generic flows are useful once a user wants to understand
composition.

### Epistemic design

This is the plugin's strongest layer. VERIFY refuses to claim success without
external evidence; RESEARCH looks for contrary material; ACH checks evidence
dependence and treats its result as least-inconsistent rather than proven;
SOURCE-QUALITY separates source reliability from information credibility; and
transformations preserve the scope and confidence of claims. Those distinctions
should be protected even if the catalog is later simplified.

### Continuity design

Portable Markdown is a better default than pretending a skill owns durable
memory. SAVE makes the transfer explicit and user-controlled. The optional
`.dialectical/` format is responsible about privacy and provenance, but it is a
secondary host capability, not a reason to add infrastructure to the plugin.

### Overall judgment

The design is coherent, unusually careful about epistemic boundaries, and
architecturally minimal where it matters. It is also near the point where more
features would reduce usability. The next gains should come from observed
behavior, catalog simplification, and better evidence about host selection—not
from new operations or services.

## Basic-question test

The following small smoke set was reviewed against the 0.7.0 source contracts
and matching release cases. “Contract pass” means the required instruction,
negative boundary, and executable QA case exist. It is not a claim that a model
or installed ChatGPT host produced the expected response.

| Basic question | Expected behavior | Source-contract result |
|---|---|---|
| `@Dialectical start a conversation` | Ask one short question about the idea, question, or decision; require no server or storage | Pass |
| `I'm curious why familiar streets feel different at night. Let's just explore it.` | Continue ordinary conversation; no operation label, menu, or forced workflow | Pass |
| `Catch me up on what we discussed.` | Give one brief RECAP cue, then compress visible discussion without adding findings | Pass |
| `GUIDE` after several live explanations and observations | Rank three context-sensitive commands, show MORE, and execute nothing until selection | Pass |
| `Show me the cookbook.` | Display the relevant packaged recipes without starting their operations | Pass |
| `VERIFY whether our analytics definition changed last month. No source is available.` | Return unresolved and identify the missing evidence; invent no citation | Pass |
| `Package this so I can continue in a new thread.` | Give a SAVE cue and a complete Markdown handoff or real file; claim no storage that did not occur | Pass |

Review commands and observed results:

```text
python3 scripts/validate_skills.py
  PASS — 24 directly discoverable skills

python3 scripts/validate_plugin_package.py
  PASS — skills-only package

python3 scripts/validate_qa.py
  PASS — 207 definitions; 61 deferred; no behavior executed

python3 -m unittest discover -s QA/tests -v
  PASS — 54 tests
```

Configured-model status: **untested** because no evaluation credential or exact
model was configured. Installed ChatGPT status: **untested** on both desktop and
iPhone. These are the next tests required for behavioral and host confidence.

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
