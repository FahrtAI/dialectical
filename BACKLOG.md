# Dialectical backlog

Future work, proposals, and unresolved questions live here. Inclusion is not
authorization to implement or publish an item. Move an idea to Planned when
its scope and acceptance criteria are agreed; remove completed items with a
link to the change that delivered them.

## Planned

No additional implementation is committed beyond the 0.5.0 work.

## Ideas

### Migrate backlog to GitHub Issues and Projects

Replace the Markdown backlog with GitHub Issues as the individual backlog items
and a GitHub Project as the planning layer. Preserve the useful structure of the
current backlog while adding issue history, discussion, labels, links to commits
and pull requests, and board/roadmap views. Avoid maintaining both systems as
parallel sources of truth.

When scheduled, define the Project fields and workflow, migrate existing
BACKLOG.md entries into Issues without losing context, verify links and
categorization, and retire this file as the active backlog once the Project is
usable.

### Optional GUIDE behavior

Help users learn which operation fits their conversation. When explicitly
enabled, review the inquiry's current state, recommend at most one useful
operation with a short explanation, and ask before performing it. Ordinary
conversation remains primary; no suggestion is a valid outcome. Respect
declines and allow the user to turn guidance off. Do not impose a fixed path.

Acceptance criteria when scheduled: enabled/disabled behavior, useful timing,
consent before execution, no repetitive advice, and no automatic chains.
GUIDE is not implemented in 0.5.0.

### Independent observer and inexpensive model evaluation

Explore implementing GUIDE with a separate observer so its instructions and
intermediate analysis do not occupy the main conversational thread. Supply a
compact inquiry summary, relevant recent turns, an operation catalog, and prior
recommendations or declines. Return no suggestion or one reasoned recommendation;
the conversational agent presents it and waits for agreement.

Test the cheapest suitable model first, comparing recommendation usefulness,
routing accuracy, restraint, consent boundaries, latency, and total cost against
guidance performed by the main model. Do not assume that a small task needs no
reasoning or that duplicating context reduces total cost. Host delegation,
model selection, and turn-trigger support must be established before committing
to an independent observer or persistent background behavior.

### Cookbook for specific kinds of analysis

Create adaptable recipes for explaining unexpected outcomes, comparing
explanations, evaluating decisions, testing causal claims, and exploring ideas.
Each should include a concrete question, useful operations and why they fit,
a sample conversation, and common pitfalls. Show where to skip an operation
or return to ordinary discussion; recipes are not mandatory sequences.
Build on the existing examples in [docs/flows.md](docs/flows.md).

### Pro forma operation sequences

Develop a small set of reusable, pro forma approaches for combining Dialectical
operations in common situations. Examples might include moving from an initial
claim through prior-art research and challenge, comparing competing explanations
before identifying collection gaps, or distilling a long inquiry before defining
reassessment indicators.

Treat these as suggested compositions, not mandatory workflows. Document why
each operation follows the previous one, where a sequence can branch or stop,
and when ordinary conversation is preferable. Evaluate overlap with the analysis
cookbook before deciding whether these should be separate artifacts or a layer
within the cookbook.

### Behavioral evaluation runner

The repository has YAML cases and a scoring rubric but no executable runner
for model behavior or invocation traces. Implement the approach already outlined
in [QA/TEST_PLAN.md](QA/TEST_PLAN.md) when scheduled, with isolated fixtures,
recorded outputs/tool activity, independent grading, and reviewed baselines.
Static validation must remain distinct from behavior and installed-host results.

## Open questions

- **ChatGPT import failure:** the user reported “Couldn't add plugin. Try again.”
  for the 0.4.0 ZIP. Local validation did not establish the cause or a successful
  installation. Reproduce on the exact import surface, inspect the failure, and
  confirm supported packaging/install behavior before declaring it resolved.
  Desktop and iPhone acceptance tests remain required; rebuilding is not proof
  of successful installation.
- **GUIDE review timing:** which conversational checkpoints justify a review,
  and how can suggestions stay useful without interrupting exploration?
- **Observer support:** can the intended ChatGPT host invoke an isolated worker
  with a selected inexpensive model? What fallback is appropriate if it cannot?
- **License:** the repository does not yet declare one. The owner must choose
  the intended reuse and distribution terms.
