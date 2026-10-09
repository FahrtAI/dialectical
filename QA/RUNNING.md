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
The GUIDE-accept case begins with a fixed, explicit prior recommendation and
evidence. GUIDE-decline tests a recommendation generated during the run.

`--suite QA/cases/positive.yaml` or another existing corpus parses its original
schema. Undefined fixtures and unsupported capabilities are reported as deferred.
Those cases remain specifications until their fixture/provider is implemented.
This first runner supports conversation-only execution. Optional file-memory,
delegation, and live-evidence suites remain open work in GitHub issue #4.

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
no events, not that text looked harmless. Optional usage includes provider token
counts and settings. The runner captures observed temporary-directory file diffs,
latency, word counts, source hashes, Git state, outputs, and repeat number.
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
results. A behavioral pass without invocation telemetry is not a routing-trace
pass. CI checks the harness and static contracts, not model behavior.

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
