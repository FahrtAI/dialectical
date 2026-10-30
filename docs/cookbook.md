# Conversations with Dialectical

Start with what you want to understand. These recipes offer possible moves;
you can skip, reorder, branch, stop, or return to ordinary conversation at any
point. Internal reasoning techniques can help finish a requested operation;
a new objective or side effect needs authorization. This same complete recipe
set is packaged for display inside ChatGPT. Ask Dialectical for `cookbook`, the
whole cookbook, or a recipe for your situation. Viewing a recipe does not run
its operations. If unsure which move fits, ask
[GUIDE](../skills/dialectical-guide/SKILL.md), which ranks useful options and
waits for your selection.

## Check something before you share it

Opening: “This market estimate is going into the board deck tomorrow.”
Run [CHALLENGE](../skills/dialectical-challenge/SKILL.md) before the claim leaves
the conversation: what it assumes, where the number came from, and what would
make it wrong. The challenge ends with what holds up, so you know what to state
confidently and what to soften or source. Use
[VERIFY](../skills/dialectical-verify/SKILL.md) for a specific figure when
evidence is available. For an independent second look, a
[SAVE](../skills/dialectical-save/SKILL.md) cold read exports just the claim and
its evidence for a fresh chat or another model. Avoid treating a survived
challenge as verification.
Minimal move: CHALLENGE.

## Explore a new idea

Opening: “Could small neighborhood rituals make a place feel more like home?”
Talk through what you mean by ritual and belonging first. Use
[RELEVANCE](../skills/dialectical-relevance/SKILL.md) if the scope is unclear,
or [RESEARCH](../skills/dialectical-research/SKILL.md): “Find prior work on this
mechanism, including cases where it failed.” Research before a claim of novelty
can reveal different names for familiar ideas. Curiosity needs no decision.
Avoid treating resemblance to a theory as validation. Minimal move: RELEVANCE.

## Explain an unexpected outcome

Opening: “Churn increased after our redesign. What might explain it?”
Separate the observed change from its interpretation in ordinary conversation.
[HYPOTHESIZE](../skills/dialectical-hypothesize/SKILL.md) can widen a narrow set
of explanations. With actual evidence, request
[ACH](../skills/dialectical-ach/SKILL.md) to compare them. If evidence is missing,
ask [COLLECTION GAPS](../skills/dialectical-collection-gaps/SKILL.md) what would
distinguish them; that proposes collection without performing it. Ask
[TEST DESIGN](../skills/dialectical-test-design/SKILL.md) when the next need is
an executable test with measurements, controls, decision rules, and consequences.
Generation
often precedes comparison because a matrix cannot repair an omitted rival.
Avoid inferring causation from timing. Minimal move: HYPOTHESIZE.

## Test a causal claim

Opening: “Restoring export will bring churn back to 3%. Does that follow?”
Clarify the claimed effect and timing, then ask
[CAUSAL-CHAIN](../skills/dialectical-causal-chain/SKILL.md) to inspect each link.
“Which assumptions carry the prediction, and what actually supports them?”
A later [VERIFY](../skills/dialectical-verify/SKILL.md) can investigate one
empirical link if you request it. Mapping first helps target the right claim.
Unexamined assumptions are uncertain, not false; no unique linchpin does not
make a chain solid. Minimal move: CAUSAL-CHAIN.

## Turn critique into an actionable test

Opening: “We have three hypotheses and several ways each could fail. What
should we test first?” Ask
[TEST DESIGN](../skills/dialectical-test-design/SKILL.md) to translate the
claims into minimum discriminating tests. For a research program, it can expose
dependencies, define what each outcome would change, and select the next test
with the highest information value relative to effort. It may consume prior
CHALLENGE, ACH, or COLLECTION GAPS output, but no fixed sequence is required.
The resulting design is generated methodology, not evidence, and the operation
does not run the experiment or collect the data. Minimal move: TEST DESIGN.

## Make a decision under uncertainty

Opening: “Should we renew our office lease?” Start with options, values,
constraints, and what could change the choice. Use
[RELEVANCE](../skills/dialectical-relevance/SKILL.md) to identify the decision's
scope, or [COLLECTION GAPS](../skills/dialectical-collection-gaps/SKILL.md):
“Which missing evidence is consequential enough to seek before we decide?”
[INDICATORS](../skills/dialectical-indicators/SKILL.md) can define conditions
for reconsideration after a choice. Gaps concern evidence to seek now; indicators
concern developments to watch. Neither automatically researches or monitors.
Avoid pretending evidence alone determines values. Minimal move: RELEVANCE.

## Evaluate a source or claim

Opening: “This vendor says its chatbot cut tickets in half. How much weight
should I give that?” First identify the exact claim and source material.
[SOURCE-QUALITY](../skills/dialectical-source-quality/SKILL.md) assesses the
provided evidence and its independence. [VERIFY](../skills/dialectical-verify/SKILL.md)
is useful when you want external evidence on the precise proposition; source
assessment may be an internal part of that job. “Verify the claimed reduction,
including whether the comparison was fair.” A report's existence does not prove
its contents. Without evidence access, verification remains incomplete.
Minimal move: SOURCE-QUALITY for a supplied report, VERIFY for a factual check.

## Develop a strategy

Opening: “We want to grow without overwhelming support.” Explore constraints
and plausible options first. [THOUGHT EXPERIMENT](../skills/dialectical-thought-experiment/SKILL.md)
can expose implications: “Suppose signups double but staffing does not. Which
assumptions fail?” [CHALLENGE](../skills/dialectical-challenge/SKILL.md) can stress-test
a developed option; [INDICATORS](../skills/dialectical-indicators/SKILL.md) can
identify signs that would justify revision. Thought experiments generate
conditional implications, not empirical evidence. No order is required; challenge
first if a strategy already exists. Minimal move: CHALLENGE.

## Compare competing explanations

Opening: “We have three explanations and six observations. Which survives?”
First agree on the actual observations and distinguish shared source origins.
Ask [ACH](../skills/dialectical-ach/SKILL.md): “Compare these, preserve unknowns,
and identify what would change the result.” If an important source is disputed,
you may request a targeted [VERIFY](../skills/dialectical-verify/SKILL.md) before
or after comparison. ACH does not automatically gather missing facts or convert
a least-inconsistent candidate into a proven cause. Minimal move: ACH.

## Work through disagreement

Opening: “We keep disagreeing about whether remote work hurts mentoring.”
Ask what each person actually claims before trying to settle it.
[RESTATE](../skills/dialectical-restate/SKILL.md) preserves scope and qualifiers:
“Restate both positions in their strongest faithful form.”
[RELEVANCE](../skills/dialectical-relevance/SKILL.md) can reveal different questions
or values; [CHALLENGE](../skills/dialectical-challenge/SKILL.md) can test a selected
argument. Clarification before critique reduces attacks on a position nobody
holds. Agreement and rhetorical strength are not evidence. Minimal move: RESTATE.

## Preserve a long inquiry

Opening: “I'm losing track of what we learned.”
[RECAP](../skills/dialectical-recap/SKILL.md) compresses what was discussed;
[DISTILL](../skills/dialectical-distill/SKILL.md) separates findings, generated
ideas, and uncertainty; [TRACE](../skills/dialectical-trace/SKILL.md) preserves
important pivots. [SAVE](../skills/dialectical-save/SKILL.md) packages the
relevant conversation as reusable Markdown that can be downloaded where the
host supports files, copied elsewhere, or imported into a new thread. No
cross-chat memory or persistence is assumed merely because the handoff was
produced. Minimal move: RECAP for coverage, DISTILL for takeaways, or SAVE for a
portable handoff. Do not make an old conclusion stronger when it is reused.
