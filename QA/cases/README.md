# Dialectical QA cases

The case corpus is split by polarity:

- `smoke.yaml` is the complete multi-turn execution subset for contract regressions
  and comparison. See [running evaluations](../RUNNING.md). Legacy suites remain
  specifications where required fixtures or host capabilities are unavailable.
- `release.yaml` is the smaller release-focused subset for material behavior
  changes; it avoids file, worker, live-evidence, and installed-host prerequisites.

- `positive.yaml` checks that the general catalog activates for intended
  requests and performs the selected operations; newer focused suites may add
  their own positive cases.
- `negative.yaml` checks that each skill stays inactive for a neighboring or
  ordinary request. Most negative cases name the operation that should handle
  the request instead.
- `delegation.yaml` checks when isolated workers should or should not be used,
  what context they receive, who synthesizes the answer, and who may mutate
  durable state.
- `chatgpt.yaml` checks startup through @Dialectical and conversation-only
  continuity on desktop and iPhone without a service or app connection.
- `help_flows.yaml` checks HELP, the complete cookbook, and generic pathways.
- `guide_palette.yaml` checks ranked GUIDE choices, MORE, and selection consent.
- `join.yaml` checks JOIN against substantial, partial, absent, and adversarial
  prior context on desktop and iPhone.
- `save_handoff.yaml` specifies portable Markdown exports and reuse of a
  representative handoff in a fresh thread. Full export-then-import continuity
  is an installed-host acceptance check.
- `response_contract.yaml` checks natural-language learning cues,
  concise-by-default output, requested depth, and evidence calibration across
  transformations and operation boundaries.
- `hold_or_update.yaml` checks that pressure without evidence or argument does
  not move an assessment, that a genuine new argument does, that earlier
  assistant agreement is corrected rather than treated as evidence, and that a
  well-supported claim is not given manufactured doubt. Run it under all three
  conditions; it is the focused regression for the hold-or-update principle.
- `test_design.yaml` checks actionable test matrices, dependencies, decision
  rules, execution boundaries, and routing against adjacent operations.

Filesystem and isolated-worker cases are optional capability suites. They do
not create prerequisites for ordinary ChatGPT conversation.

Positive and negative do not mean good and bad user sentiment. They describe
whether the skill under test should activate.

GUIDE coverage includes explicit and conversational invocation, three ranked
commands, complete MORE expansion, insufficient context, numeric and named
selection, ignored menus, and separation from orientation, direct operations,
ordinary conversation, and background-observer requests. GUIDE does not execute
before selection, offer a sequence, monitor later turns, or create tools or
workers.

The corpus also covers RELEVANCE, COLLECTION GAPS, TEST DESIGN, and INDICATORS individually,
including ordinary phrasing, exploratory and decision purposes, ambiguity,
collection history, absent signals, justified thresholds, and neighboring-skill
boundaries. Positive cases need only the supplied conversation, without tools,
prior operations, or storage. Negative cases also check that HYPOTHESIZE and
ACH behavior does not trigger an additional skill. TEST DESIGN cases distinguish
designing a discriminating future test from identifying a gap, surfacing a
failure mode, adjudicating existing evidence, or conducting the research.

## Case fields

- `id`: stable case identifier.
- `skill`: skill being tested.
- `mode`: `explicit`, `implicit`, `contextual`, or `negative`.
- `prompt`: user input presented to the model.
- `environment`: fixture or capability assumptions.
- `expect_activation.include`: skills that must activate.
- `expect_activation.exclude`: skills that must not activate.
- `expect`: observable requirements for the response or artifacts.
- `forbid`: behaviors that cause the case to fail.
- `expected_mutation`: allowed mutation class and paths.
- `expect_delegation`: expected decision, worker count, role, and context
  boundaries when the case exercises isolated workers.

The activation fields require a structured trace. The runner compares them with
adapter `invocations` telemetry. A run without that telemetry cannot pass its
routing assertion; installed-host routing still requires host acceptance.

Each production routing or behavior failure should become a new case. Do not
rewrite an old case merely to make a changed implementation pass unless the
underlying product contract intentionally changed.
