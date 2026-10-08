---
name: dialectical-guide
description: Recommend at most one useful Dialectical operation for the current conversational state. Use when the user explicitly invokes GUIDE or directly asks which Dialectical operation would help now; do not activate merely because an operation might be useful, monitor later turns, or perform the recommendation.
metadata:
  version: "0.6.0"
---

# Guide

Help the user choose one useful move without taking over the conversation.
GUIDE is invoked on demand; it is not a background mode or observer.

## Operation

1. Review the inquiry's current state using only available context: what the
   user is trying to understand or decide, the claims and alternatives in play,
   the evidence already available, and the present obstacle.
2. First consider whether ordinary conversation should continue. A formal
   operation is useful only when it would address a specific current need.
3. If one operation would materially help, recommend only that operation. Name
   the concrete feature of the conversation that makes it fit, state briefly
   what the operation would contribute, and preserve the boundary of its job.
4. End by asking whether the user wants to try it. Do not perform it in the same
   response. Agreement on a later turn authorizes that operation only.
5. If no operation would materially help, say so briefly and suggest continuing
   the conversation. If context is too thin to judge, ask one brief question
   about what feels stuck or what the user wants from the conversation.

Use the operation distinctions in
[`../dialectical/references/help.md`](../dialectical/references/help.md). In
particular:

- use RELEVANCE for unclear purpose or scope, COLLECTION GAPS for evidence to
  seek, RESEARCH for seeking it, INDICATORS for developments to watch, and
  VERIFY for adjudicating one empirical proposition;
- use HYPOTHESIZE when the explanatory space is narrow and ACH when real
  alternatives and evidence are ready to compare;
- use CHALLENGE to stress-test a position, CAUSAL-CHAIN to inspect its causal
  links, and SOURCE-QUALITY to assess a source;
- use SUMMARIZE for a compact recap and DISTILL when the intellectual state has
  become difficult to hold; and
- recommend lifecycle or memory operations only when continuity or persistence
  is the user's present need.

## Response shape

Keep the intervention conversational rather than presenting a diagnostic
report. A useful response normally contains:

- the recommendation, or a clear statement that no operation is needed;
- one or two sentences tied to the current conversation; and
- when recommending an operation, a short consent question.

## Boundaries

- Do not recommend multiple operations, a sequence, or a complete workflow.
- Do not execute the recommendation, browse, delegate, persist anything, or
  create monitoring or scheduled work.
- Do not continue evaluating later turns unless GUIDE is invoked again.
- Do not treat a declined recommendation as permission to propose another.
- Do not invoke GUIDE recursively or substitute the full help card for a
  contextual recommendation.
- Keep GUIDE in the conversational agent. OBSERVER is a separate future idea
  and is not required for this operation.
