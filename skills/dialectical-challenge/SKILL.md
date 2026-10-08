---
name: dialectical-challenge
description: Subject a claim, explanation, plan, or emerging consensus to adversarial quality control. Use to surface assumptions, contradictions, alternatives, disconfirming evidence, and failure conditions; do not use for reflexive contrarianism or stylistic criticism.
metadata:
  version: "0.6.0"
---

# Challenge

Try to break the current thinking in ways that improve its reliability.

Structured methods are available when the challenge calls for them. Name the method whenever you apply one:

- `dialectical-ach` when the user requests ACH or several explanations must be compared against multiple observations.
- `dialectical-causal-chain` when the position rests on a multi-step causal argument.
- `dialectical-source-quality` when the challenge turns on how much weight particular sources deserve.

## Operation

1. Identify the exact claim or model under challenge and state its strongest reasonable form.
2. Test its key assumptions, internal consistency, causal logic, boundary conditions, and fit with available evidence.
3. Consider credible alternatives and evidence that is inconsistent with the current view. Use ACH when several explanations and diagnostic observations make that rigor useful.
4. Describe plausible failure modes and what conditions would produce them.
5. Distinguish fatal problems, material weaknesses, and ordinary uncertainties.
6. State what evidence, revision, or test would most strengthen or overturn the position.

Target the highest-leverage vulnerabilities. A challenge is successful when it reveals how the idea could fail, not when it merely sounds skeptical.

## Delegation

For a substantive challenge, default to an isolated worker when the host supports one. Supply the strongest formulation, relevant evidence, user goal, and material constraints, while omitting unrelated social or rhetorical context that could anchor the critique. Ask for vulnerabilities, mechanisms, failure conditions, and disconfirming evidence—not a polished response to the user. The conversational agent checks that the worker attacked the real position, removes performative objections, and owns the final answer. Challenge a short or context-dependent claim directly when delegation would add no useful independence.

## Boundaries

- Do not attack a weaker version of the position than the conversation supports.
- Do not manufacture objections with no plausible mechanism or consequence.
- Do not treat missing evidence as evidence of absence without justification.
- Do not silently resolve empirical disputes; invoke VERIFY or RESEARCH when external evidence is required.
