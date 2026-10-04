# Dialectical QA cases

The case corpus is split by polarity:

- `positive.yaml` checks that each skill activates for an intended request and
  performs its own operation.
- `negative.yaml` checks that each skill stays inactive for a neighboring or
  ordinary request. Most negative cases name the operation that should handle
  the request instead.

Positive and negative do not mean good and bad user sentiment. They describe
whether the skill under test should activate.

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

The activation fields require a structured trace. Until the runner captures
skill invocation events, they may be scored manually while the output and
filesystem assertions are evaluated.

Each production routing or behavior failure should become a new case. Do not
rewrite an old case merely to make a changed implementation pass unless the
underlying product contract intentionally changed.
