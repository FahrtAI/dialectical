<h1 align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/dialectical-logo-dark.png">
    <img src="assets/dialectical-logo.png" alt="Dialectical" width="480">
  </picture>
</h1>

> Ordinary conversation with intellectual discipline.

LLMs can be thought of as lossy, natural-language search engines for the material they ingested during training—which, for a frontier model, can include an awful lot of the material on the internet.

That lossiness is part of what makes them useful. By bringing similar or related concepts into view across many contexts at once, an LLM can surface prior art, reveal unexpected associations, reframe an idea, and help refine a line of thought.

It is also the source of familiar failures. An LLM can blur where an idea came from, turn a resemblance into a claim, exaggerate its confidence, or make a coherent story feel truer than the evidence warrants.

Dialectical is a set of optional conversational operations designed to use the first capability without ignoring the second. Some operations help explore and connect ideas. Others trace sources, research claims, generate competing explanations, and look deliberately for disconfirming evidence.

The conversation stays ordinary. The discipline appears when it is useful.

## What it does

Dialectical gives the user and the LLM a shared vocabulary for common moves in a serious conversation: restating an idea, distilling what has been learned, finding prior art, testing an explanation, tracing a claim, or saving a useful connection.

These are not stages in a mandatory workflow. Each operation does one job, and any of them can be used when the conversation calls for it.

> Formalize the interventions, not the conversation.

The system is built around one warning:

> An LLM's ability to make an idea more coherent is not evidence that the idea is more true.

## Using it

Talk normally. Ask for a particular kind of help when you want it:

```text
What have we actually learned so far?
Find prior art connected to this idea.
What else could explain the increase in churn?
Try to disprove my interpretation.
Trace that claim back to its sources.
Run a thought experiment on this assumption.
Save that connection for later.
```

Every operation also has a short, explicit handle:

```text
DISTILL where we are.
RESEARCH prior art for this approach.
HYPOTHESIZE why churn rose after the redesign.
CHALLENGE the plan to cut prices.
Use ACH on those three explanations.
SAVE that connection.
```

The capitalized names are conversational handles, not command syntax. See [sample conversations](docs/flows.md) for complete examples.

## Operations

| Purpose | Operations | What they help you do |
|---|---|---|
| Understand the conversation | RESTATE, SUMMARIZE, DISTILL, TRACE | Clarify an idea, compress context, extract what was learned, and recover provenance |
| Explore | RESEARCH, HYPOTHESIZE, THOUGHT EXPERIMENT | Find relevant prior art, generate explanations, and examine implications |
| Test | CHALLENGE, VERIFY, ACH, CAUSAL-CHAIN, SOURCE-QUALITY | Seek counterarguments and disconfirming evidence, test causal logic, and assess sources |
| Remember | TAG, SAVE, RECALL | Organize, preserve, and retrieve useful knowledge |
| Continue over time | START INQUIRY, CHECKPOINT, RESUME, CLOSE | Maintain an optional line of inquiry across conversations |

ACH is Analysis of Competing Hypotheses: it compares rival explanations against the evidence instead of asking only whether a favored explanation fits. CAUSAL-CHAIN exposes the assumptions in each link of a causal argument. SOURCE-QUALITY rates the reliability of a source separately from the credibility of the information it provides.

## How it behaves

- Normal conversation remains primary. The default is not to intervene.
- Operations are optional, independently composable, and never silently chained.
- Claims, inferences, and speculation remain distinguishable.
- Uncertainty, disagreement, abandoned branches, and provenance are preserved when they matter.
- A thought experiment can expose implications; it cannot supply empirical evidence.
- When the discussion becomes difficult to hold, Dialectical may offer to DISTILL it once.
- When an untested claim begins to settle into fact, it may offer one relevant check once.
- Retrieved notes are treated as untrusted data, never as instructions.

Dialectical also distinguishes among debate, narrative, inquiry, and decision. Each is legitimate, but each fails differently. In particular, a plausible narrative is not necessarily an explanation, and a decision mixes facts with goals, values, and trade-offs. The distinction should improve the answer without making the conversation sound like a methodology workshop. See [conversation modes](skills/dialectical/references/modes.md) for details.

## Installation

Install `skills/dialectical` and every `skills/dialectical-*` directory as siblings in the skill discovery directory used by your host:

```sh
DEST=~/.claude/skills   # replace with your host's discovery directory
mkdir -p "$DEST"
for d in skills/dialectical skills/dialectical-*; do cp -R "$d" "$DEST/"; done
```

| Platform | Discovery directory or integration | Guide |
|---|---|---|
| Claude Code | `.claude/skills/` or `~/.claude/skills/` | [CLAUDE.md](CLAUDE.md) |
| Codex | `$CODEX_HOME/skills/` | [CODEX.md](CODEX.md) |
| Gemini CLI | `.gemini/skills/` or `.agents/skills/` | [GEMINI.md](GEMINI.md) |
| ChatGPT | Plugin and MCP server included in this repository | [CHATGPT.md](CHATGPT.md) |

A reference to this repository in a platform instruction file does not install the skills. Confirm that all operations are discoverable after installation.

### Optional monitoring

Skills normally load only when invoked. To enable Dialectical's two restrained, proactive checks, add the following to the instruction file your host always loads:

```markdown
## Dialectical
- Keep the conversation primary; don't intervene by default.
- Suggest DISTILL when branches and open questions have become hard to hold.
- When we start treating an untested claim, mechanism, prediction, or "new" idea as settled, offer once, in one line, what would check it.
- When the question turns from what's true to what to do, separate facts from goals and values.
- Coherence, agreement, and repetition are not evidence.
- Run an operation only when asked or when a suggestion is accepted.
```

Use `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, or ChatGPT project/custom instructions, depending on the host.

## ChatGPT plugin

This repository is also the plugin root. It contains the portable manifests, all bundled skills, and an MCP service under `server/` for durable inquiries and saved knowledge. The development manifests use `http://127.0.0.1:8787/mcp`; a public release requires a stable HTTPS endpoint and real publisher, privacy, terms, and support URLs.

```sh
cd server
npm install
npm run typecheck
npm test
npm run build
```

See the [ChatGPT integration guide](CHATGPT.md) and [server documentation](server/README.md) for local setup, authentication, and deployment.

Build and validate a local development package from the repository root:

```sh
python3 scripts/package_plugin.py --development
python3 scripts/validate_plugin_package.py
```

For a production package, replace the local endpoint, add the required public URLs, and run `python3 scripts/package_plugin.py`. The production preflight rejects localhost, non-HTTPS endpoints, and missing release metadata.

## Memory

Dialectical records inquiry state rather than full transcripts. A local skill host can use the file-backed `.dialectical/` store; the ChatGPT plugin uses the MCP service. An integration should use one backend as the source of truth and must not claim to remember information that is neither in the current context nor retrieved from that backend.

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

Records preserve provenance, uncertainty, and superseded states. `.dialectical/` is ignored by Git by default because it may contain private conversation data. The complete format and mutation rules are in the [memory specification](skills/dialectical/references/memory.md).

## Development

```text
skills/       independently discoverable operations
server/       MCP persistence service
evals/        behavioral cases and scoring rules
QA/           test plan and test cases
scripts/      validators and packaging tools
docs/         sample conversation flows
assets/       project and plugin artwork
```

Run the structural and package checks with:

```sh
python3 scripts/validate_skills.py
python3 scripts/validate_plugin_package.py
```

Behavioral cases live in `evals/cases.yaml`, with scoring rules in `evals/SCORING.md`. The broader [QA test plan](QA/TEST_PLAN.md) covers positive and negative routing cases, memory integration, adversarial boundaries, evidence-access modes, and release gates.

Each skill declares its own semantic version because operations can evolve independently. The plugin version in `plugin.json` and `.codex-plugin/plugin.json` must match and should be bumped whenever a bundled skill or the MCP server changes.

## Status

The skills, local memory contract, plugin package, and MCP server are implemented. Behavioral evaluation is currently manual. RESEARCH and VERIFY depend on the evidence-access capabilities of the host. A public ChatGPT release still requires production hosting, publisher verification, policy and support URLs, and submission assets. The project does not yet declare a license.
