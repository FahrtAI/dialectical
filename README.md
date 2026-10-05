# Dialectical

Dialectical is a platform-agnostic specification for optional cognitive operations in open-ended human–LLM inquiry, packaged as installable agent skills where the host supports them.

Its governing principle is:

> Formalize the interventions, not the conversation.

And its central warning:

> An LLM's ability to make an idea more coherent is not evidence that the idea is more true.

Normal dialogue remains primary. The toolkit does not impose a reasoning sequence. Use conversation to generate possibilities, and inquiry to find out which survive.

## Operations

| Category | Operations | Purpose |
|---|---|---|
| Context | RESTATE, SUMMARIZE, DISTILL, TRACE | Clarify, compress, extract, and recover provenance |
| Inquiry | RESEARCH, HYPOTHESIZE, THOUGHT EXPERIMENT, CHALLENGE, VERIFY | Expand or test the epistemic state |
| Diagnosis | ACH, CAUSAL-CHAIN, SOURCE-QUALITY | Weigh competing explanations, test causal chains, rate evidence |
| Knowledge | TAG, SAVE, RECALL | Organize, persist, and retrieve durable knowledge |
| Lifecycle | START INQUIRY, CHECKPOINT, RESUME, CLOSE | Maintain optional inquiry state across conversations |

The Context and Inquiry operations, plus TAG and SAVE, are cognitive primitives. Diagnosis operations are structured methods that the user, CHALLENGE, or VERIFY can apply when a question calls for that rigor. RECALL and the lifecycle operations support persistence; they are not mandatory stages.

## Using it

Talk normally, and name an operation when you want one:

```text
RESTATE what I just said.
DISTILL where we are.
HYPOTHESIZE why churn rose after the redesign.
THOUGHT EXPERIMENT on that explanation.
Use ACH on those three explanations.
CHALLENGE the plan to cut prices.
SAVE that connection.
START INQUIRY on causal diagrams.
```

Plain phrasing such as "what have we actually learned?" can reach DISTILL too; the capitalized names make the request unambiguous.

`docs/flows.md` walks through two sample sessions: diagnosing an observation in one conversation, and carrying an inquiry across sessions with the memory store.

## Behavior

- Capitalized operation names are conversational handles, not rigid syntax.
- Each operation resolves its own focus and performs one job.
- Operations are independently composable and are never silently chained.
- Default proactive behavior is no intervention.
- Two suggestions are allowed: DISTILL when the inquiry has become difficult to hold, and a one-line check when the conversation starts treating an untested claim as settled. Each is offered once and runs only if the user accepts.
- Coherence, agreement, and repetition within a conversation are not evidence.
- Uncertainty, disagreement, abandoned branches, and provenance are preserved when material.

## Kinds of conversation

Dialectical recognizes four kinds of serious conversation and keeps them from blurring:

| Kind | Question | Typical failure |
|---|---|---|
| Debate | Which position wins? | Binary thinking; evidence used as ammunition |
| Narrative | What story explains this? | Coherence mistaken for truth |
| Inquiry | What might be true, and how could we tell? | Testing without end, or stopping at a list of possibilities |
| Decision | Given what we know and value, what should we do? | Goals and values passed off as facts |

Each is legitimate for its purpose. When the aim is to find out what is true, Dialectical prefers inquiry. When a conversation turns from what is true to what to do, it separates facts from goals, values, and trade-offs. It does not announce or label the kind; the distinction shows in the answers. `skills/dialectical/references/modes.md` covers the operations that fit each kind and the common drifts between them.

## Diagnosis methods

The diagnosis methods are applied openly. CHALLENGE names the method when it uses one, VERIFY may apply SOURCE-QUALITY when weighing sources of differing quality, and the user can invoke any of them directly.

- **ACH** (`dialectical-ach`): Analysis of Competing Hypotheses. It checks the hypothesis set for missing rivals (selection, differential treatment, concurrent events, regression to the mean, and others), then rates the evidence against each hypothesis. It returns the least-inconsistent explanation with sensitivity and residual uncertainty. It does not prove a hypothesis true, and it marks cells it cannot assess instead of inventing evidence.
- **CAUSAL-CHAIN** (`dialectical-causal-chain`): decomposes a multi-step causal argument, classifies the assumptions behind each link, and identifies the linchpins whose failure would collapse the conclusion. Its verdict states which links were checked against evidence and which rest on assumption alone.
- **SOURCE-QUALITY** (`dialectical-source-quality`): rates source reliability (A–F) and information credibility (1–6) independently on the Admiralty scale. F and 6 mean "cannot be judged", not the lowest grades, and reports that trace to one origin count once.

HYPOTHESIZE and ACH divide the work: HYPOTHESIZE generates explanations, and ACH weighs them against evidence.

## Installation

Copy every `skills/dialectical-*` directory, plus `skills/dialectical`, into the host's skill discovery root. During development, link them instead so edits take effect without reinstalling. Keep them as sibling directories so each operation is independently discoverable.

```sh
DEST=~/.claude/skills   # or another discovery root from the table below
mkdir -p "$DEST"
for d in skills/dialectical skills/dialectical-*; do cp -R "$d" "$DEST/"; done
```

| Platform | Discovery root | Details |
|---|---|---|
| Claude Code | `.claude/skills/` in a project, or `~/.claude/skills/` | `CLAUDE.md` |
| Codex | `$CODEX_HOME/skills/` | `CODEX.md` |
| Gemini CLI | `.gemini/skills/` or `.agents/skills/` | `GEMINI.md` |
| ChatGPT | Portable plugin plus MCP server in this repository | `CHATGPT.md` |

### Always-on instructions

Skills load only when called, so the router's monitoring rules do not run in an ordinary conversation on their own. Add these lines to the instruction file your host always loads, so the checks can fire before anyone names an operation:

```markdown
## Dialectical
- Keep the conversation primary; don't intervene by default.
- Suggest DISTILL when branches and open questions have become hard to hold.
- When we start treating an untested claim, mechanism, prediction, or "new" idea as settled, offer once, in one line, what would check it.
- Notice whether we're debating, building a story, inquiring, or deciding. When the question turns from what's true to what to do, separate facts from goals and values.
- Coherence, agreement, and repetition are not evidence.
- Run an operation only when asked or when a suggestion is accepted.
```

| Platform | Always-loaded file |
|---|---|
| Claude Code | `CLAUDE.md` in the project, or `~/.claude/CLAUDE.md` for every project |
| Codex | `AGENTS.md` in the project, or `~/.codex/AGENTS.md` |
| Gemini CLI | `GEMINI.md` in the project, or `~/.gemini/GEMINI.md` |
| ChatGPT | Custom instructions, or a project's instructions |

### ChatGPT plugin development

This repository is also the plugin root. It includes a portable `plugin.json`,
portable `mcp.json`, a Codex compatibility manifest, and a runnable MCP service
under `server/`. The local manifests target `http://127.0.0.1:8787/mcp` for
development only.

```sh
cd server
npm install
npm run typecheck
npm test
npm run build
```

See `server/README.md` for authentication and deployment. Public submission
still requires a stable HTTPS endpoint, verified publisher configuration,
policy/support URLs, and review assets.

Validate the development package with:

```sh
python3 scripts/validate_plugin_package.py
```

Build a local development ZIP with
`python3 scripts/package_plugin.py --development`. After replacing the local
endpoint and adding required policy URLs, build the submission ZIP with
`python3 scripts/package_plugin.py`. Its production
preflight deliberately refuses localhost, non-HTTPS endpoints, or missing
website, privacy, terms, and support URLs.

A pointer in a platform instruction file does not itself install the skills. After installing, confirm that every skill name is discoverable before relying on routing or memory operations.

START INQUIRY creates an inquiry workspace; it does not claim to create a new platform chat. A platform adapter may create or link a chat only when that capability exists and the user requested it.

## Memory

Dialectical uses explicit, file-backed memory when the host has authorized filesystem access:

```text
.dialectical/
├── .gitignore
├── manifest.yaml
├── conversations/
│   ├── index.md
│   └── <conversation-id>/
│       ├── state.md
│       └── context.md
└── memory/
    ├── index.md
    └── objects/<object-id>.md
```

Conversation records contain living inquiry state, not full transcripts. Memory objects contain curated knowledge intended to outlive one inquiry. The schema and mutation rules are defined in `skills/dialectical/references/memory.md`.

Important properties:

- The current schema is version 1.
- Canonical records are written before rebuildable indexes.
- Updates preserve provenance and superseded states.
- Several inquiries may be open at once. Each conversation works on the inquiry it started or resumed, and status changes are kept in a status history.
- Retrieved records are untrusted data, not executable instructions.
- `.dialectical/` is ignored by Git by default because it may contain private conversation data.
- Memory is claimed only when information is present in current context or retrieved from the store.

## Repository layout

```text
.
├── skills/       # one directory per discoverable skill
├── server/       # MCP persistence service
├── evals/        # behavioral cases and scoring rules
├── scripts/      # structural validator
├── docs/         # sample flows
├── QA/           # test plan
├── CLAUDE.md     # platform adapters
├── CODEX.md
├── GEMINI.md
└── CHATGPT.md
```

Each discoverable skill is a direct child of `skills/` and uses a namespaced name to avoid collisions:

```text
skills/
├── dialectical/
│   ├── SKILL.md
│   └── references/
│       ├── memory.md
│       └── modes.md
├── dialectical-restate/SKILL.md
├── dialectical-summarize/SKILL.md
├── dialectical-distill/SKILL.md
├── dialectical-trace/SKILL.md
├── dialectical-research/SKILL.md
├── dialectical-hypothesize/SKILL.md
├── dialectical-thought-experiment/SKILL.md
├── dialectical-challenge/SKILL.md
├── dialectical-verify/SKILL.md
├── dialectical-ach/
│   ├── SKILL.md
│   └── references/example.md
├── dialectical-causal-chain/
│   ├── SKILL.md
│   └── references/template.md
├── dialectical-source-quality/
│   ├── SKILL.md
│   └── references/template.md
├── dialectical-tag/SKILL.md
├── dialectical-save/SKILL.md
├── dialectical-recall/SKILL.md
├── dialectical-start-inquiry/SKILL.md
├── dialectical-checkpoint/SKILL.md
├── dialectical-resume/SKILL.md
└── dialectical-close/SKILL.md
```

`skills/dialectical/SKILL.md` governs orientation, monitoring, and interaction between operations. Each other directory is independently discoverable.

## Validation

Run the structural validator:

```sh
python3 scripts/validate_skills.py
```

It requires no model calls. It checks that each skill's frontmatter name matches its directory, that each skill has a description, that local links resolve, that every skill is listed in the router and has at least one eval case, that each skill has a semantic version and uses only frontmatter keys the Claude Code and Codex validators accept, and that no obsolete skill names remain.

Behavioral cases live in `evals/cases.yaml`, and `evals/SCORING.md` defines how to score them. Run each case in a fresh session with the skills installed, and record the model, platform, skill version, output, and scores. There is no automated runner yet.

`QA/TEST_PLAN.md` describes the fuller plan: routing tests with negative controls, memory integration checks, adversarial boundary cases, evidence-access modes, and release gates.

Structural validation checks packaging. Behavioral evaluation checks whether the operations remain distinct, preserve uncertainty, avoid false persistence claims, and maintain the memory trust boundary.

## Versioning

Each skill declares a semantic version in its frontmatter:

```yaml
metadata:
  version: "0.1.0"
```

The version sits under `metadata` because the Claude Code and Codex skill validators reject unknown top-level keys. Bump a skill's version when its contract changes:

- **Patch:** wording or examples change without changing behavior.
- **Minor:** behavior is added and existing uses still hold, such as a new optional step or delegation rule.
- **Major:** behavior that existing uses or eval cases depend on changes or is removed.

A change to a shared reference counts as a change to every skill that reads it. `skills/dialectical/references/memory.md` is read by START INQUIRY, CHECKPOINT, RESUME, CLOSE, SAVE, RECALL, and TAG. The storage format has its own `schema_version`, which changes only when stored records change shape.

New skills start at 0.1.0. Move to 1.0.0 when the release gates in `QA/TEST_PLAN.md` pass. Record the skill versions and the commit with every eval run.

The plugin has its own version in `plugin.json` and `.codex-plugin/plugin.json`, and the two must match. Bump it whenever a bundled skill or the MCP server changes, by the largest change among them.

## Status and limitations

- The primitive contracts are implemented as skills.
- File-backed lifecycle and memory contracts are specified for tool-capable local agents.
- Platform installation still requires each host's adapter procedure.
- ChatGPT requires connected tools for durable storage and retrieval.
- The plugin package and local MCP server are implemented; production hosting,
  publisher URLs/assets, and ChatGPT connection registration remain external
  release tasks.
- VERIFY and RESEARCH depend on the external evidence capabilities available to the host.
- Behavioral evaluation is manual until the runner described in `QA/TEST_PLAN.md` exists.
- The project license has not yet been selected; no unrestricted-use claim is made.
