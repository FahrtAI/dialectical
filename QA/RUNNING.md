# Running evaluations

Requires Python 3.10+ and PyYAML in the maintainer environment. The installed
plugin has no Python or dependency requirement.

```sh
python3 scripts/run_evals.py validate
python3 scripts/validate_qa.py --json
python3 -m unittest discover -s QA/tests
```

The default suite is `QA/cases/smoke.yaml`. It contains complete inputs and
multi-turn cases; later user turns follow the actual generated assistant output.
The GUIDE-accept case begins with a fixed ranked menu and supplied evidence;
the user then names one command. GUIDE-decline tests a ranked menu generated
during the run and confirms that ignoring it authorizes no operation.

`--suite QA/cases/positive.yaml` or another existing corpus parses its original
schema. Undefined fixtures and unsupported capabilities are reported as deferred.
Those cases remain specifications until their fixture/provider is implemented.
The focused runner supports conversation-only execution. Optional file-memory,
delegation, live-evidence, and installed-host suites remain separate capability
work; they are not required by the lightweight regression harness.

For a material behavior release, use the smaller
`QA/cases/release.yaml` subset first. It covers ordinary conversation,
natural-language cues, GUIDE consent, JOIN, concision, calibration, SAVE, and
no-evidence VERIFY without requiring files, workers, live evidence, or an
installed ChatGPT host. For changes to the hold-or-update principle, also run
`QA/cases/hold_or_update.yaml` under the ordinary, brief, and dialectical
conditions. Add a focused regression case when a release changes a
different critical behavior; do not turn every specification case into a model
gate.

## Adapter protocol

Use an explicitly selected trusted adapter executable. It receives one JSON
request on stdin per turn: `protocol_version`, `instructions`, `messages`, and
`capabilities`. Expectations and grading criteria are withheld from the performer.
Use the same model and generation settings for every condition. The adapter must
honor the supplied instruction condition and disable evidence, file, and worker
tools. Each case uses a fresh temporary working directory. This directory is
isolation for fixtures, not an OS security sandbox; use a sandboxed adapter for
strong containment. Do not run untrusted adapters.

Return one JSON object on stdout:

```json
{"response":"Actual model output", "model":"exact-model-id", "usage":null,
 "tool_activity":null, "invocations":null}
```

Use null when telemetry is unavailable. An empty list means the adapter observed
no events, not that text looked harmless. Each `invocations` item is either a
skill-name string or an object with a nonempty `skill` field. When a case has
`expect_activation`, unavailable telemetry leaves the run ungraded and a trace
that contradicts its include/exclude lists fails. Optional usage includes
provider token counts and settings. The runner captures observed
temporary-directory file diffs, latency, word counts, source hashes, Git state,
outputs, and repeat number.
It does not observe writes outside that directory or prove installed-host routing.
Adapters should be stateless: each request includes the full conversation.

```sh
python3 scripts/run_evals.py run --condition dialectical --repeat 3 \
  --output QA/runs/dialectical.json \
  --adapter /absolute/path/to/model-adapter \
  --grader /absolute/path/to/independent-grader
```

No provider credentials or model choice are guessed. The adapter is development
infrastructure supplied by the evaluator, never a server the plugin depends on.
Failure and timeout records are retained. The runner never overwrites an existing
artifact. Raw runs are Git-ignored; deliberately selected, reviewed artifacts
belong in `QA/baselines/` after checking for private data.

## Optional configured OpenAI adapter

`scripts/adapters/openai_responses.py` is one practical maintainer adapter for
the [OpenAI Responses API](https://platform.openai.com/docs/api-reference/responses/create).
It uses Python's standard library, configures no tools, disables response
storage, and remains outside the installable ZIP. It never chooses a model or
credential silently. Set the key and both exact model identifiers in the
environment; do not put credentials in command arguments or run artifacts.

```sh
export OPENAI_API_KEY='...'
export DIALECTICAL_EVAL_MODEL='exact-performer-model-id'
export DIALECTICAL_GRADER_MODEL='exact-grader-model-id'

python3 scripts/run_evals.py run \
  --suite QA/cases/release.yaml \
  --condition dialectical \
  --repeat 3 \
  --output QA/runs/0.8.0-release.json \
  --adapter python3 scripts/adapters/openai_responses.py \
  --grader python3 scripts/adapters/openai_grader.py
```

The adapter records API usage when returned, the requested and returned model,
provider-default generation settings, duration, and that no tools were
configured. It reports invocation telemetry as unavailable because prompt
injection does not expose installed-host skill loading. A semantic result may be
graded, but it must not be described as an installed-host routing pass. Use
`QA/RELEASE_ACCEPTANCE.md` for actual ChatGPT invocation.

The exact merged case definitions and adapter/grader commands are embedded in
each run artifact alongside source hashes, Git state, transcripts, usage,
latency, tool activity, invocation telemetry, and grader output.

Compare two retained runs with:

```sh
python3 scripts/compare_runs.py QA/runs/baseline.json QA/runs/candidate.json \
  --output QA/runs/comparison.md
```

The report aligns cases and shows status, routing trace, mean response words,
reported tokens, duration, and rubric score. Review transcripts and rationales;
lower token count or latency is not by itself an improvement.

## Grading

The independent grader gets the actual transcript, expectations, forbidden
behaviors, and [canonical rubric](../evals/SCORING.md), with condition labels
withheld. Model wording may still reveal the condition. It returns:

```json
{"scores": {
 "routing":{"score":2,"reason":"Evidence from the transcript"},
 "operation":{"score":2,"reason":"Evidence from the transcript"},
 "calibration":{"score":2,"reason":"Evidence from the transcript"},
 "boundary":{"score":2,"reason":"Evidence from the transcript"},
 "usefulness":{"score":2,"reason":"Evidence from the transcript"}},
 "critical_violation":false}
```

Human-review material grading disagreements and critical cases. An ungraded run
is not a pass. Exit status is nonzero for error, failure, deferred, or ungraded
results. A behavioral response without invocation telemetry is not a passing
routing trace. CI checks the harness and static contracts, not model behavior.

For releases with material skill-behavior changes, run the release subset after
static validation and before installed-host acceptance. Keep a failing, timed
out, deferred, or ungraded result visibly non-passing. #11's three-condition
comparative quality study is separate research and is not implied by this
regression run.

## Comparison and recorded manual runs

Use `ordinary`, `brief`, and `dialectical` conditions. Ordinary has no added
methodology; brief uses `QA/conditions/brief.txt`; Dialectical injects the current
entry skills plus help/modes references. This controls instruction content but
does not test host skill discovery or loading latency. All conditions receive
identical task messages and evidence limits. Report explicit Dialectical-handle
cases separately from natural-language comparisons.

For manual runs, retain the same case IDs, exact user/assistant turns, condition,
model/host identity, repeat number, and unavailable telemetry as null. Score in
a separate pass; do not synthesize transcripts from expected outcomes. Document
when multiple cases share an evaluator context: those are pilot observations,
not independent fresh sessions. Report all failures, word-count tradeoffs,
suggestion repetition, and variation; don't infer superiority from a tiny pilot.
