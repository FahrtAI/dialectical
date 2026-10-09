# 0.6.1 development pilot

Collected October 8, 2026; reviewed October 9, 2026. These are development
observations, not installed-host acceptance or a production efficacy baseline.

## Method and provenance

Three independent Codex agents received the same eight selected smoke scenarios:
ordinary exploration, GUIDE acceptance, GUIDE decline, causal analysis without
a unique linchpin, evidence-scope distillation, challenge composition,
conversation-only continuity, and verification without evidence access.

- A: ordinary conversation, no added methodology instructions.
- B: the fixed short discipline prompt in `QA/conditions/brief.txt`.
- C: revised Dialectical entrypoints plus help/modes instructions.

Exact delivered instructions and case messages are preserved in `pilot-inputs.json`;
the C snapshot still bears 0.6.0 frontmatter because the mechanical 0.6.1 version
bump followed preparation of that bundle. The behavior changes were already in it.
Outputs are `pilot-A.json`, `pilot-B.json`, and `pilot-C.json`. A separate agent
read those labeled samples, the case expectations, and the canonical rubric,
without the condition mapping or skill instructions. Its judgments and rationales
are preserved in `pilot-grades.json`. The main agent checked prompt/transcript
integrity and reviewed the recorded outputs and grading observations.

The evaluator used inherited platform instructions in every condition. Cases
within each agent shared context and were simulated sequential exchanges; there
was one run per condition, no randomization, and no independently repeated fresh
session per case. Exact backend model, generation settings, latency, token usage,
tool traces, and actual skill-invocation events were unavailable. Null telemetry
means unavailable, not an observed absence. Instruction injection does not test
host discovery. No same-model cost or performance claim can be made from this run.

## Observations

| Condition | Cases recorded | Independent grader passes | Assistant words |
|---|---:|---:|---:|
| Ordinary | 8 | 8 | 1,316 |
| Brief prompt | 8 | 8 | 1,345 |
| Dialectical | 8 | 8 | 1,752 |

Word counts exclude fixed fixture assistant messages and include whitespace-separated
table syntax. All recorded cases received 10/10 from the independent grader and
no visible critical violation. This is a ceiling effect in a small, relatively
easy suite, not proof of equivalence or superiority. No sample repeated the
declined method suggestion, claimed durable persistence, or invented an ordinance
verdict. Dialectical gave more explicit source qualifications and causal structure,
but used about 33% more words than ordinary conversation here. Detail is a cost
as well as a possible benefit; the pilot did not establish better user outcomes.

Review concerns: C's ACH matrix uses a broad measurement-change column whose
query-change inconsistency is narrower than the column label; its prose explains
the distinction, but a skim-reader could miss it. C's challenge calls the target
a reversal of an increase even though that history is not supplied in that case.
The grader treated that as minor framing imprecision. Preserve both observations
for harder follow-up cases rather than silently editing the captured responses.

## Next measurement

Run the four unobserved smoke cases (convergence, supported parallel path,
explicit combined request, and record injection), then at least three independent
fresh-session repeats per condition using one identified model/configuration.
Add longer ambiguous conversations and unseen transfer examples fixed before
viewing outcomes; review disagreements with a human. Assess whether added detail
changes decisions or preserves uncertainty better, and report negative results.
Issue #11 remains open until this stronger comparison is complete. OBSERVER #2
remains deferred: the pilot did not identify a failure requiring another agent.
