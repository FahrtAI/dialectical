---
name: dialectical-distill
description: Extract the important findings, conclusions, uncertainties, and open questions produced by an inquiry, marking which rest on evidence and which the conversation only generated. Use when the user asks what has actually been learned or when the intellectual state has become difficult to hold; do not use for a general recap.
metadata:
  version: "0.4.0"
---

# Distill

Convert accumulated conversation into a clear account of its present intellectual state.

## Operation

1. Resolve the relevant conversational span and central inquiry.
2. Separate what the inquiry supports from what was merely mentioned or proposed. Mark the basis of every finding:
   - **Established:** shown directly by evidence from outside the conversation's own reasoning, such as sources consulted or data and records the user supplied.
   - **Tested:** a hypothesis or inference that was checked against such evidence and survived. Name the test.
   - **Generated:** hypothesized, inferred, or argued in the conversation, but not checked against evidence.
   - **Speculative:** raised as a possibility with little support.

   Coherence, agreement, and repetition within the conversation do not move a claim from generated to tested.
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

- Do not retell the whole conversation; that is SUMMARIZE.
- Do not make generated or speculative ideas sound established, however persuasive or often repeated they were.
- Do not automatically research, verify, challenge, or save the result.
- Do not force a conclusion when the genuine result is sharper uncertainty.
- Perform this in the conversational agent, which owns the inquiry's epistemic state; do not delegate it to a worker with partial context.
