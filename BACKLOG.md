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

### On-demand GUIDE operation

Create GUIDE as an explicitly invoked operation for moments when a free-form
conversation would benefit from a little more structure. GUIDE reviews the
current inquiry and recommends at most one Dialectical operation or thinking
technique that could sharpen the discussion, with a short explanation of why it
fits. It may also conclude that no structured intervention is useful right now.

GUIDE does not monitor the conversation, impose a workflow, or automatically
execute the recommended operation. The user remains in ordinary conversation
unless they deliberately call GUIDE and choose to act on its recommendation.

### Optional OBSERVER subagent

Explore OBSERVER as a separate, opt-in capability that runs alongside the main
conversation and watches for moments when a structured-thinking intervention
might be useful. OBSERVER may surface a suggestion using the same recommendation
logic as GUIDE, but it should not execute an operation or turn the conversation
into a prescribed process.

Evaluate whether the intended ChatGPT host can support an isolated subagent,
appropriate review timing, compact context handoff, and inexpensive model
selection. Compare usefulness, restraint, latency, and total cost against the
explicit GUIDE operation. GUIDE should remain independently useful even if
OBSERVER is never implemented.

### Cookbook and operation checklists

Create adaptable checklists for recurring kinds of analysis such as explaining
unexpected outcomes, comparing explanations, evaluating decisions, testing
causal claims, and exploring ideas. Each should begin with a concrete question
and identify useful Dialectical operations, why they fit, and combinations that
often work well together.

These are prompts for thinking, not prescribed processes. A user or model may
start in the middle, skip an operation, branch, stop, double back, or return to
ordinary conversation. Document useful ordering where it matters, but explain
the reasoning rather than implying that one operation must mechanically follow
another. Include sample conversations and common pitfalls. Build on the existing
examples in [docs/flows.md](docs/flows.md).

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
- **OBSERVER review timing:** which conversational checkpoints justify a review,
  and how can suggestions stay useful without interrupting exploration?
- **OBSERVER support:** can the intended ChatGPT host invoke an isolated worker
  with a selected inexpensive model? What fallback is appropriate if it cannot?
- **License:** the repository does not yet declare one. The owner must choose
  the intended reuse and distribution terms.
