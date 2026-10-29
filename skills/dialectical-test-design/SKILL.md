---
name: dialectical-test-design
description: Convert an empirical claim, hypothesis, model, or research program into discriminating tests with explicit measurements, controls, dependencies, decision rules, and consequences. Use when the user asks how to test an idea or turn critique or missing evidence into an actionable research plan; do not use only to identify gaps, judge existing evidence, or conduct the research.
metadata:
  version: "0.8.0"
---

# Test Design

Turn an unresolved empirical claim into a plan that can change the inquiry.

Use the shortest complete response that makes the proposed test executable and
its interpretation auditable. For a clear ordinary-language invocation that
does not name TEST DESIGN, begin with one line:
`TEST DESIGN — <brief context-specific description>.` Omit the cue for an
explicit command, mere discussion, or an internal technique used by another
operation.

## Operation

1. State the exact claim or competing hypotheses to be tested. Preserve their
   scope, qualifiers, and current epistemic status. Split a broad program only
   where different claims require materially different evidence.
2. Identify the consequential failure mechanism, rival explanation, or
   ambiguity the test must discriminate. Use supplied CHALLENGE, ACH, or
   COLLECTION GAPS results when available, but do not require those operations
   or silently run them as separate objectives.
3. Choose the smallest feasible design that can distinguish meaningful
   outcomes. It may be an experiment, quasi-experiment, observational study,
   benchmark, robustness check, source-collection plan, or measurement study.
   Prefer information gained over procedural completeness.
4. Operationalize what will be observed: units, conditions, measurements,
   timing, comparison or baseline, and the controls needed for the main
   confounds or artifacts. Distinguish a proxy from the construct it is meant
   to represent.
5. Define the decision rule before the result is known. State what outcomes
   would support, weaken, reject, or leave the claim unresolved. Do not invent
   numerical thresholds, sample sizes, or practical-significance cutoffs when
   the context cannot justify them; identify what must set them instead.
6. Expose dependencies and order tests so that downstream claims do not rest on
   failed measurements or assumptions. For a program, identify the next test
   with the highest expected information value relative to cost, time, and
   reversibility.
7. State the consequence of each material outcome: what would be retained,
   revised, dropped, investigated next, or used as a stopping condition.

For one claim, concise prose may be enough. For a larger program, use a matrix
when it improves comparison. Useful columns are:

| Claim | Failure mechanism | Minimum discriminating test | Measurement and controls | Decision rule | Dependency | Consequence |
|---|---|---|---|---|---|---|

Include only columns that change the design. A polished matrix is not a
substitute for a discriminating test or an explicit decision rule.

## Relationship to other operations

- **CHALLENGE** asks how a position could fail; TEST DESIGN turns a selected
  vulnerability into a test and decision rule.
- **ACH** compares competing explanations against available evidence; TEST
  DESIGN specifies how to obtain evidence that would distinguish them.
- **COLLECTION GAPS** identifies missing evidence worth seeking; TEST DESIGN
  specifies how the evidence should be produced or measured and interpreted.
- **VERIFY** adjudicates a proposition against available external evidence;
  TEST DESIGN proposes future work and does not perform or adjudicate it.

## Delegation

Keep ordinary test design in the conversational agent so it can preserve the
inquiry's claims, constraints, and decision consequences. For a consequential
or technically complex design, an isolated worker may review one bounded issue
such as confounding, measurement validity, or statistical identifiability when
the host supports it. The conversational agent reconciles the review and owns
the design; independent reviewers do not make the proposed evidence independent.

## Boundaries

- A test plan is **generated**, not evidence that a claim has been tested.
- Do not collect data, browse for evidence, run an experiment, or mutate a
  system unless the request separately authorizes that work.
- Do not optimize a design only to confirm the favored claim. Include outcomes
  that could materially weaken it or distinguish a credible rival.
- Do not call an association causal unless the design supports that inference.
- Do not hide infeasibility behind an elaborate protocol. Name unavailable
  measurements, ethical limits, weak proxies, and underidentified questions.
- Do not turn every inquiry into a research program; scale the design to the
  user's actual decision and available effort.
