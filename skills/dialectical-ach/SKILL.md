---
name: dialectical-ach
description: Evaluate competing explanations against the available evidence using Analysis of Competing Hypotheses and identify the least-inconsistent one. Use when the user requests ACH or several explanations must be compared against multiple observations; do not use only to generate explanations (HYPOTHESIZE) or to adjudicate one proposition (VERIFY).
metadata:
  version: "0.9.0"
---

# ACH

Identify the explanation least contradicted by the available evidence. ACH does not prove a hypothesis true.

Use the shortest complete response that preserves material evidence, source
dependence, uncertainty, and the limits of the candidate set. For a clear
ordinary-language invocation that does not name ACH, begin with one line:
`ACH — <brief context-specific description>.` Omit the cue for explicit ACH,
mere discussion, or use as an internal technique. Change a claim's scope or
confidence only when the stated evidence or analysis justifies it.

## Operation

### Frame

1. State the observation or decision to be explained without embedding a favored answer.

### Complete the hypothesis set

2. Start from the hypotheses the user or conversation already has. Treat a favored explanation as one candidate, not the default.
3. Check the set for missing rivals. Ask whether each of these could produce the same observation:
   - **Selection or composition:** the groups or periods differed before the event.
   - **Differential treatment:** one group was handled differently after the event.
   - **Measurement artifact:** the metric signals something other than what it is taken to mean.
   - **Comparison-group contamination:** the comparison group is diluted or defined differently.
   - **Concurrent events:** something else changed at the same time.
   - **Regression to the mean:** an extreme starting value would have moved back regardless.
   - **Reverse causation:** the outcome drove the supposed cause.
   - **Measurement change:** tracking, definitions, or instrumentation changed.
   - **Chance:** the difference is within normal variation.

   Add a rival only when it has a plausible mechanism for this observation. Skip categories that do not apply; the list is a check, not a quota.
4. Make overlaps between hypotheses explicit. When causes can combine, frame each hypothesis as the main source of the effect. Do not create cosmetic variants to fill a matrix.

### Evaluate

5. List material evidence, including absences, assumptions, source limitations, and observations that would normally be expected but are missing.
6. Check whether evidence items share an underlying source or mechanism. Do not count correlated repetitions as independent support.
7. Rate each evidence–hypothesis pair:
   - `++` strongly consistent
   - `+` consistent
   - `0` neutral or non-diagnostic
   - `-` inconsistent
   - `--` strongly inconsistent
   - `?` insufficient information
8. Weight diagnostic evidence, which fits some hypotheses and not others, above evidence compatible with all of them. Focus on contradictions rather than counting supporting marks. One reliable contradiction may matter more than many weak consistencies.
9. Seek plausible evidence that would disconfirm the leading hypothesis. Reassess after adding it.
10. Run a sensitivity check: identify which uncertain evidence or weighting could change the result.
11. Select the least-inconsistent hypothesis. If the evidence does not separate the leaders, say so rather than choosing one.

### Choose the next test

12. Recommend the evidence that would most change the result. Prefer the most diagnostic test; among comparably diagnostic tests, prefer the cheaper. A rival that is cheap to test and still untested is a high testing priority, not a more credible hypothesis.

## Delegation

For a large matrix, the conversational agent remains the manager of one canonical hypothesis set, evidence set, and rating standard. When isolated workers are available, delegate bounded checks such as testing one hypothesis against the shared evidence or auditing evidence independence. Give every worker the same relevant definitions and evidence, and require it to mark missing information rather than invent it. Reconcile the results into one matrix; do not combine separately framed matrices or let workers vote on the winner. Analyze a small matrix directly.

## Output

- the observation and hypotheses, marking rivals added in step 3;
- the evidence matrix;
- source-dependence and diagnosticity notes;
- the least-inconsistent assessment, or a statement that the evidence does not separate the leaders;
- sensitivity and residual uncertainty;
- the next most discriminating test.

A worked example is in [`references/example.md`](references/example.md).

## Boundaries

- Do not present the least-inconsistent hypothesis as proven.
- Do not invent evidence to fill cells; mark them `?`.
- Do not total symbols mechanically.
- Do not substitute generating explanations for evaluating them; generation alone is HYPOTHESIZE.
- When the matrix depends on external facts that are not available, say so; do not silently run RESEARCH or VERIFY.
