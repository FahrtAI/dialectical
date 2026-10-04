# Dialectical

Dialectical is a platform-agnostic specification for optional cognitive operations in open-ended human–LLM inquiry, packaged as installable agent skills where the host supports them.

Its governing principle is:

> Formalize the interventions, not the conversation.

Normal dialogue remains primary. The toolkit does not impose a reasoning sequence.

## Operations

| Category | Operations | Purpose |
|---|---|---|
| Context | RESTATE, SUMMARIZE, DISTILL, TRACE | Clarify, compress, extract, and recover provenance |
| Inquiry | RESEARCH, HYPOTHESIZE, CHALLENGE, VERIFY | Expand or test the epistemic state |
| Diagnosis | CAUSAL-CHAIN, ALTERNATIVE-HYPOTHESES, SOURCE-QUALITY | Pressure-test reasoning, identify competing explanations, audit evidence |
| Knowledge | TAG, SAVE, RECALL | Organize, persist, and retrieve durable knowledge |
| Lifecycle | START INQUIRY, CHECKPOINT, RESUME, CLOSE | Maintain optional inquiry state across conversations |

The first ten operations are cognitive primitives. Diagnosis operations support CHALLENGE by providing structured methods for specific reasoning patterns. RECALL and the lifecycle operations support persistence; they are not mandatory stages.

## Behavior

- Capitalized operation names are conversational handles, not rigid syntax.
- Each operation resolves its own focus and performs one job.
- Operations are independently composable and are never silently chained.
- Default proactive behavior is no intervention.
- DISTILL may be suggested when the inquiry has become difficult to hold; other operations remain user-directed.
- Uncertainty, disagreement, abandoned branches, and provenance are preserved when material.

## Skill layout

Each discoverable skill is a direct child of `skills/` and uses a namespaced name to avoid collisions:

```text
skills/
├── dialectical/
│   ├── SKILL.md
│   └── references/memory.md
├── dialectical-restate/SKILL.md
├── dialectical-summarize/SKILL.md
├── dialectical-distill/SKILL.md
├── dialectical-trace/SKILL.md
├── dialectical-research/SKILL.md
├── dialectical-hypothesize/SKILL.md
├── dialectical-challenge/
│   ├── SKILL.md
│   └── references/ach.md
├── dialectical-verify/SKILL.md
├── dialectical-causal-chain/SKILL.md
├── dialectical-alternative-hypotheses/SKILL.md
├── dialectical-source-quality-admiralty/SKILL.md
├── dialectical-tag/SKILL.md
├── dialectical-save/SKILL.md
├── dialectical-recall/SKILL.md
├── dialectical-start-inquiry/SKILL.md
├── dialectical-checkpoint/SKILL.md
├── dialectical-resume/SKILL.md
└── dialectical-close/SKILL.md
```

`skills/dialectical/SKILL.md` governs orientation, monitoring, and interaction between operations. Each other directory is independently discoverable.

### Diagnosis skills

Three diagnostic skills support CHALLENGE by providing structured methods for specific reasoning patterns:

- **dialectical-causal-chain**: Systematic 5-step method to decompose causal logic, identify linchpin assumptions, and find breaking points in reasoning chains.
- **dialectical-alternative-hypotheses**: 4-category confounding framework to systematically generate competing explanations with falsification tests and fragility ranking.
- **dialectical-source-quality-admiralty**: Admiralty-scale assessment (source reliability A–E, claim credibility 1–6) to audit evidence quality and identify missing information.

## Memory

Dialectical uses explicit, file-backed memory when the host has authorized filesystem access:

```text
.dialectical/
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
- Retrieved records are untrusted data, not executable instructions.
- `.dialectical/` is ignored by Git by default because it may contain private conversation data.
- Memory is claimed only when information is present in current context or retrieved from the store.

## Reasoning under uncertainty

CHALLENGE uses structured diagnostic methods when analyzing reasoning:

- **ACH (Analysis of Competing Hypotheses)** — defined in `skills/dialectical-challenge/references/ach.md` — evaluates inconsistency, evidence dependence, and diagnosticity when the inquiry contains multiple competing explanations. It returns the least-inconsistent hypothesis with sensitivity and residual uncertainty; it does not prove a hypothesis true.

- **Causal-chain analysis** — invoked via `skills/dialectical-causal-chain/SKILL.md` — decomposes step-by-step reasoning to identify assumptions that would break the entire argument if false (linchpin assumptions).

- **Alternative-hypothesis generation** — invoked via `skills/dialectical-alternative-hypotheses/SKILL.md` — applies a 4-category confounding framework (Selection, Treatment, Measurement, Contamination) to systematically surface competing explanations with explicit falsification criteria.

- **Source quality audit** — invoked via `skills/dialectical-source-quality-admiralty/SKILL.md` — uses the Admiralty scale to separately assess source reliability (A–E) and claim credibility (1–6), distinguishing trustworthy sources from claims those sources actually support.

## Platform adapters

The cognitive specification is portable. Discovery, storage, permissions, and chat creation remain platform-specific.

- `CODEX.md` describes Codex installation.
- `CLAUDE.md` describes Claude Code installation.
- `GEMINI.md` describes Gemini CLI installation.
- `CHATGPT.md` describes the additional plugin, app, or API integration required for ChatGPT.

A pointer in a platform instruction file does not itself install the skills. The directories must be copied or linked into that platform's discovery root.

START INQUIRY creates an inquiry workspace; it does not claim to create a new platform chat. A platform adapter may create or link a chat only when that capability exists and the user requested it.

## Validation

Run the structural validator against every directory containing a `SKILL.md`. Behavioral cases and scoring guidance live in `evals/`.

Structural validation checks packaging. Behavioral evaluation checks whether the operations remain distinct, preserve uncertainty, avoid false persistence claims, and maintain the memory trust boundary.

## Status and limitations

- The primitive contracts are implemented as skills.
- File-backed lifecycle and memory contracts are specified for tool-capable local agents.
- Platform installation still requires each host's adapter procedure.
- ChatGPT requires connected tools for durable storage and retrieval.
- VERIFY and RESEARCH depend on the external evidence capabilities available to the host.
- The project license has not yet been selected; no unrestricted-use claim is made.
