---
name: dialectical-distill
description: Extract the important findings, conclusions, uncertainties, and open questions produced by an inquiry, marking which rest on evidence and which the conversation only generated. Use when the user asks what has actually been learned or when the intellectual state has become difficult to hold; do not use for a general recap.
metadata:
  version: "0.7.0"
---

# Distill

Convert accumulated conversation into a clear account of its present intellectual state.

Use the shortest complete response that preserves material evidence,
provenance, disagreement, uncertainty, and the exact status of each finding.
For a clear ordinary-language invocation that does not name DISTILL, begin with
one line: `DISTILL — <brief context-specific description>.` Omit the cue for an
explicit command or mere discussion. Change a claim's scope or confidence only
when the stated evidence or analysis justifies it.

## Operation

1. Resolve the relevant conversational span and central inquiry.
2. Separate what the inquiry supports from what was merely mentioned or proposed. Mark the basis of every finding:
   - **Established:** the exact, limited observation directly supported by inspected evidence. A supplied record can establish what it reports without establishing that its contents are accurate, causal, representative, or independently verified. Retain provenance and material limitations.
   - **Tested:** a hypothesis or inference checked against identified evidence. Name the test, its scope, its outcome, and what remains unresolved; surviving a limited test does not establish the whole explanation.
   - **Generated:** hypothesized, inferred, or argued in the conversation, but not checked against evidence.
   - **Speculative:** raised as a possibility with little support.

   Coherence, agreement, and repetition within the conversation do not move a claim from generated to tested.
   A VERIFY verdict or ACH ranking keeps its original scope and uncertainty.
   Do not promote "least inconsistent among these candidates" into "the cause,"
   or a source's assertion into an independently established fact.
3. Extract the smallest set of consequential insights, decisions, live uncertainties, and open questions.
4. Preserve confidence levels and disagreements. Do not manufacture consensus.
5. Identify what changed relative to the inquiry's starting point when that change is meaningful.

Use only the sections that contain useful material:

- What is established or tested
- What we generated but have not tested
- What remains uncertain
- Open questions
- Consequences or next decisions

Favor intellectual signal over transcript coverage.

## Boundaries

- Do not retell the whole conversation; that is RECAP.
- Do not make generated or speculative ideas sound established, however persuasive or often repeated they were.
- Do not automatically research, verify, challenge, or save the result.
- Do not force a conclusion when the genuine result is sharper uncertainty.
- Perform this in the conversational agent, which owns the inquiry's epistemic state; do not delegate it to a worker with partial context.
