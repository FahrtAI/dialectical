---
name: dialectical-causal-chain
description: Decompose a multi-step causal argument into its links, expose the assumptions each link needs, and identify the linchpins whose failure would collapse the conclusion. Use when the user asks to test a chain of reasoning in which each step depends on the previous one; do not use for a single correlation or for general critique (CHALLENGE).
metadata:
  version: "0.5.1"
---

# Causal Chain

Find where a chain of reasoning would break.

## Operation

1. Map the chain as stated: `A → B → C → outcome`. Keep the argument's own steps and wording; do not repair it while mapping. Mark any step the argument leaves implicit as inferred.
2. For each link, ask what must be true for it to hold. Check these kinds of assumption where they are relevant:
   - **Priority:** this is the main driver, not a minor one.
   - **Necessity:** this means is required, not one of several alternatives.
   - **Direction:** A drives B, not the reverse, and no third factor drives both.
   - **Transfer:** what held in one setting holds in this one.
   - **Timing:** each step can happen in the time the argument allows.
   - **Barriers:** completing one step actually removes the obstacles to the next.
3. Classify each assumption by what happens if it is false:
   - **Linchpin:** the conclusion fails, and no other path reaches it.
   - **Load-bearing:** the conclusion survives but becomes much less likely.
   - **Minor:** one link weakens, but other paths remain.

   Most assumptions are not linchpins. Reserve the label for those whose failure leaves no route to the conclusion.
4. Test each link: whether its mechanism is stated or only asserted, whether causation is shown or assumed, whether the next step could happen without this one, whether a confounder could produce both, and what observation would show the link is false.
5. Identify the weakest link and the linchpins, and give a verdict with its basis, stating which links were checked against evidence and which rest on assumption alone:
   - **Solid:** every linchpin is supported by evidence.
   - **Vulnerable:** a linchpin is unexamined, or several load-bearing assumptions are doubtful.
   - **Brittle:** a linchpin is doubtful or contradicted by evidence.

For a loop (A → B → A), find the initial trigger and analyze forward from it; the key question is whether the trigger is strong enough to start the cycle. When several independent chains reach the same outcome, analyze each separately and ask which one is operating. When timing is unstated, check whether the durations are compatible; a step that needs longer than the argument allows weakens that link unless the steps can overlap.

A template and worked example are in [`references/template.md`](references/template.md).

## Delegation

When a chain is long, branching, or difficult to separate from the conversation's preferred conclusion, an isolated worker may map and test it using only the exact chain, relevant evidence, timing constraints, and verdict definitions. The conversational agent preserves one canonical chain and reconciles the worker's analysis with conversational context. Do not split a serial chain across workers whose steps depend on one another; analyze a short chain directly.

## Boundaries

- Do not attack a weaker version of the chain than the argument supports.
- Do not mark an assumption false without evidence; mark it unexamined.
- Do not list every conceivable assumption; prioritize those that would change the conclusion.
- Do not silently resolve empirical questions about a link; say what evidence is needed. Gathering it is VERIFY or RESEARCH.
- Do not weigh rival explanations against evidence here; that is ACH.
