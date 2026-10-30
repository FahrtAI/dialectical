<h1 align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/dialectical-logo-dark.png">
    <img src="assets/dialectical-logo.png" alt="Dialectical" width="480">
  </picture>
</h1>

> Ordinary conversation with intellectual discipline.

**Current version:** 0.8.0 (skills-only)

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

Install the plugin, select **Dialectical** from ChatGPT's `@` menu, and send
`@Dialectical start a conversation`. It asks what you want to explore and begins
in the current chat. No external server, account connection, or database is required.

Talk normally. Ask for a particular kind of help when you want it:

Start with a familiar need: explore an idea, test an explanation, check a claim,
or recover what you learned. You do not need to learn the operation catalog.
The [cookbook](docs/cookbook.md) gives short examples for these and other situations.

```text
What have we actually learned so far?
Find prior art connected to this idea.
What else could explain the increase in churn?
Try to disprove my interpretation.
Turn these hypotheses into decisive tests.
Trace that claim back to its sources.
Run a thought experiment on this assumption.
Save that connection for later.
JOIN this existing conversation.
```

Every operation also has a short, explicit handle:

```text
GUIDE: which operation would help now?
DISTILL where we are.
RESEARCH prior art for this approach.
HYPOTHESIZE why churn rose after the redesign.
CHALLENGE the plan to cut prices.
TEST DESIGN the smallest experiment that could change our minds.
Use ACH on those three explanations.
SAVE that connection.
```

The capitalized names are conversational handles, not command syntax. See [sample conversations](docs/flows.md) for complete examples.

When an ordinary-language request clearly selects an operation, Dialectical
briefly names it before answering—for example, `RECAP — Catching up on the
discussion.` This is a one-line learning cue, not a confirmation step or method
lecture. Ordinary conversation and internal reasoning techniques are not labeled
as separate operations.

Dialectical-specific help uses a compact, stable [command card](skills/dialectical/references/help.md) rather than generating a new introduction each time.

## Operations

| Purpose | Operations | What they help you do |
|---|---|---|
| Choose a move | GUIDE | Rank three useful commands for the current conversational state, or show the full catalog |
| Understand the conversation | RESTATE, RECAP, DISTILL, TRACE | Clarify an idea, compress context, extract what was learned, and recover provenance |
| Frame an inquiry | RELEVANCE, COLLECTION GAPS, INDICATORS | Clarify purpose, prioritize missing evidence, and define developments worth watching |
| Explore | RESEARCH, HYPOTHESIZE, THOUGHT EXPERIMENT | Find relevant prior art, generate explanations, and examine implications |
| Test | CHALLENGE, TEST DESIGN, VERIFY, ACH, CAUSAL-CHAIN, SOURCE-QUALITY | Seek counterarguments, design discriminating tests, adjudicate claims, test causal logic, and assess sources |
| Preserve and reuse | TAG, SAVE, RECALL | Organize knowledge, export a Markdown handoff, and retrieve accessible records |
| Continue over time | START INQUIRY, CHECKPOINT, RESUME, CLOSE | Maintain an optional line of inquiry across conversations |

ACH is Analysis of Competing Hypotheses: it compares rival explanations against the evidence instead of asking only whether a favored explanation fits. CAUSAL-CHAIN exposes the assumptions in each link of a causal argument. SOURCE-QUALITY rates the reliability of a source separately from the credibility of the information it provides.

GUIDE is an on-demand palette, not a mode. It considers the current conversation,
ranks three useful commands, and offers MORE for the complete catalog. It waits
for a numeric or named selection and runs only that command. GUIDE does not
monitor later turns or perform anything before selection.

Use `@Dialectical JOIN` after invoking Dialectical in an existing conversation.
When the host provides meaningful prior context, JOIN offers RECAP, DISTILL,
TRACE, or CONTINUE and waits for a choice. It cannot retrieve unseen messages or
attach itself retroactively outside the host's normal plugin interface.

SAVE packages the relevant conversation as a self-contained Markdown handoff.
Upload or paste that handoff into a new thread to continue. A downloadable file
is used when the host supports it; otherwise SAVE returns complete copyable
Markdown. It does not imply automatic cross-thread memory.

Ask “What are we trying to understand?” for RELEVANCE, “What evidence would
distinguish these explanations?” for COLLECTION GAPS, “How exactly would we
test these hypotheses?” for TEST DESIGN, or “What should we watch
for that would change our assessment?” for INDICATORS. Each is independently
callable. Exploration does not require a decision or a formal inquiry setup.
COLLECTION GAPS identifies missing evidence; TEST DESIGN turns a claim or gap
into measurements, controls, decision rules, and consequences; RESEARCH seeks
evidence; VERIFY checks a specific empirical claim. TEST DESIGN does not conduct
the proposed research, and INDICATORS does not create monitoring or scheduled tasks.

## How it behaves

- Normal conversation remains primary. The default is not to intervene.
- Responses default to the shortest complete answer; requested depth and
  consequential evidence, provenance, disagreement, or uncertainty are not
  sacrificed for brevity.
- Operations are optional, independently composable, and never silently chained.
- GUIDE is invoked explicitly, ranks three commands, and waits for one selection.
- Claims, inferences, and speculation remain distinguishable.
- A transformation preserves a claim's supported scope and confidence unless
  new evidence or explicit analysis justifies a stated change; calibration is
  not blanket skepticism.
- Uncertainty, disagreement, abandoned branches, and provenance are preserved when they matter.
- A thought experiment can expose implications; it cannot supply empirical evidence.
- When the discussion becomes difficult to hold, Dialectical may offer to DISTILL it once.
- When an untested claim begins to settle into fact, it may offer one relevant check once.
- Retrieved notes are treated as untrusted data, never as instructions.

Dialectical also distinguishes among debate, narrative, inquiry, and decision. Each is legitimate, but each fails differently. In particular, a plausible narrative is not necessarily an explanation, and a decision mixes facts with goals, values, and trade-offs. The distinction should improve the answer without making the conversation sound like a methodology workshop. See [conversation modes](skills/dialectical/references/modes.md) for details.

## Install in ChatGPT

See [CHATGPT.md](CHATGPT.md) for account installation, desktop and iPhone tests,
and the distinction between a local folder and an installed account plugin.
Use the skills-only ZIP in `dist/dialectical-0.8.0.zip`.
Installing this source does not automatically update an older account plugin.

The portable package contains `plugin.json`, `LICENSE`, `skills/`, and referenced artwork.
Its OpenAI display name is **Dialectical**. The plugin includes no MCP
configuration, app dependency, executable runtime, or service.

## Continuity

Conversation works without storage. SAVE returns a portable Markdown handoff; CHECKPOINT
returns a state note; RESUME can use a checkpoint you paste or attach.
The plugin does not promise automatic recall across chats.

For hosts with an authorized filesystem, the existing optional `.dialectical/`
format remains supported. It is private and Git-ignored by default. See the
[memory reference](skills/dialectical/references/memory.md).
RESEARCH and VERIFY use available evidence tools or sources you supply; without
them they state the limitation instead of inventing citations.

## Development

These existing maintainer utilities validate and package files; users do not
run them to conduct a conversation:

```sh
python3 scripts/validate_skills.py
python3 scripts/validate_plugin_package.py
python3 scripts/package_plugin.py
```

Every CI build retains a ZIP, checksum, and source record. Version-tag builds
prepare a draft GitHub release from the tested artifacts. See
[building and releasing](docs/releases.md) for reproducible builds, tag/version
checks, and the post-install smoke test.

Behavioral evaluation is separate: see [QA/RUNNING.md](QA/RUNNING.md) for the
focused release subset, complete smoke fixtures, optional configured-model
adapter, canonical rubric, and recorded-run comparison. The runner is a
maintainer utility and is excluded from the plugin.

The ZIP includes only the manifest, license, skill Markdown files, and referenced
plugin icons. Repository documentation, tests, and build utilities stay outside it.

```text
plugin.json   portable plugin manifest
skills/       entry skill, focused operations, and supporting references
assets/       project and plugin artwork
QA/           release acceptance checklist and the hold-or-update behavioral suite
evals/        scoring rubric for behavioral runs
scripts/      static checks and ZIP packaging
docs/         examples and architecture audit
CHATGPT.md    installation and device testing
LICENSE       CC BY-NC-SA 4.0 legal terms
```

Package validation runs in CI. Installed-host acceptance follows
[QA/RELEASE_ACCEPTANCE.md](QA/RELEASE_ACCEPTANCE.md); behavioral runs are
described in [QA/RUNNING.md](QA/RUNNING.md). See the [architecture audit](docs/architecture-audit.md)
for the removal of the old service dependency and official specification links.

All 25 bundled skills use release version 0.8.0. Storage schema versions are
separate and have not changed. Other optional host guides remain in
[CLAUDE.md](CLAUDE.md), [CODEX.md](CODEX.md), and [GEMINI.md](GEMINI.md).

## License

Dialectical—including its methodology, skills, documentation, assets, and
utility code—is licensed by FahrtAI under the
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
License](LICENSE), unless a file states otherwise. Reuse requires attribution,
is limited to noncommercial purposes, and adaptations must use the same license.

SPDX identifier: `CC-BY-NC-SA-4.0`.

## Status

Future work, design questions, and ideas are tracked in the
[Dialectical GitHub Project](https://github.com/orgs/FahrtAI/projects/1).

The skills-only package can be built locally. Successful local validation does
not establish account installation, public directory approval, or desktop/iPhone
behavior. Record those tests after installing the updated plugin.
