# Dialectical QA cases

The case corpus is split by polarity:

- `positive.yaml` checks that each skill activates for an intended request and
  performs its own operation.
- `negative.yaml` checks that each skill stays inactive for a neighboring or
  ordinary request. Most negative cases name the operation that should handle
  the request instead.
- `delegation.yaml` checks when isolated workers should or should not be used,
  what context they receive, who synthesizes the answer, and who may mutate
  durable state.
- `chatgpt.yaml` checks startup through @Dialectical and conversation-only
  continuity on desktop and iPhone without a service or app connection.

Filesystem and isolated-worker cases are optional capability suites. They do
not create prerequisites for ordinary ChatGPT conversation.

Positive and negative do not mean good and bad user sentiment. They describe
whether the skill under test should activate.

The 0.5.0 cases cover RELEVANCE, COLLECTION GAPS, and INDICATORS individually,
including ordinary phrasing, exploratory and decision purposes, ambiguity,
collection history, absent signals, justified thresholds, and neighboring-skill
boundaries. Their positive cases need only the supplied conversation, without
tools, prior operations, or storage. Negative cases also check that existing
HYPOTHESIZE and ACH behavior does not trigger an additional skill.

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

The activation fields require a structured trace. Until the runner captures
skill invocation events, they may be scored manually while the output and
filesystem assertions are evaluated.

Each production routing or behavior failure should become a new case. Do not
rewrite an old case merely to make a changed implementation pass unless the
underlying product contract intentionally changed.
