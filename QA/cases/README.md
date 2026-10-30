# Dialectical QA cases

`hold_or_update.yaml` is the behavioral suite. It checks that pressure without
evidence or argument does not move an assessment, that a genuine new argument
does, that earlier assistant agreement is corrected rather than treated as
evidence, and that a well-supported claim is not given manufactured doubt. Run
it under each condition described in [running evaluations](../RUNNING.md).

The earlier specification suites were removed in #35 because none had been run
against a model since the 0.6.1 pilot. Add a case here only when it will be run.

## Case fields

- `id`: stable case identifier.
- `skill`: skill being tested.
- `mode`: `explicit`, `implicit`, `contextual`, or `negative`.
- `prompt`: user input presented to the model.
- `environment`: capability assumptions; `fixture` must be `none` or `conversation-in-prompt`.
- `messages`: optional prior conversation supplied inline.
- `turns`: scripted user turns for multi-turn cases (instead of `prompt`).
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
