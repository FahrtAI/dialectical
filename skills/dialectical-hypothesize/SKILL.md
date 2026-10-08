---
name: dialectical-hypothesize
description: Generate genuinely competing explanations for an observation, pattern, or outcome and expose what would distinguish them. Use when the explanatory space is too narrow; do not use for generic brainstorming, variants of one favored story, or weighing explanations against evidence (ACH).
metadata:
  version: "0.5.1"
---

# Hypothesize

Broaden the set of plausible explanations while making the alternatives discriminable.

## Operation

1. State the observation to be explained without embedding a preferred cause in it.
2. Identify important constraints that every viable explanation must address.
3. Generate explanations that differ in mechanism, not merely wording or degree.
4. For each useful hypothesis, give:
   - the proposed mechanism;
   - what it explains well;
   - its key assumptions;
   - a distinctive prediction or observation;
   - evidence that would weaken it.
5. Include combinations only when interaction between mechanisms is itself plausible.
6. End with the most informative evidence or test for separating the leading alternatives, without declaring a winner prematurely.

The number of hypotheses should reflect the explanatory space, not an arbitrary quota.

## Delegation

When the conversation already favors an explanation and the host supports an isolated worker, use a fresh worker to reduce anchoring. Give it the neutral observation, material constraints, and output contract; omit the favored causal story unless it is necessary to understand the observation. The conversational agent combines its candidates with those already present and does not treat independence as evidence that a hypothesis is more likely. For a simple or unanchored request, generate directly.

## Boundaries

- Do not disguise minor variations of one explanation as competitors.
- Do not confuse possible with probable.
- Do not optimize only for novelty; retain plausible ordinary explanations.
- Do not verify or rank hypotheses without evidence sufficient to do so.
- Do not score hypotheses against an evidence matrix; that is ACH.
