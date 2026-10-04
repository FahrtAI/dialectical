---
name: dialectical-restate
description: Rearticulate the current claim, idea, question, or position clearly without materially changing it. Use when the user asks what they or the conversation are actually saying; do not use for compression, conclusions, critique, or reframing.
metadata:
  version: "0.1.0"
---

# Restate

Express the current object of thought more clearly while preserving its meaning.

## Operation

1. Resolve the focus from the user's reference and nearby conversation. Ask only if materially different referents remain plausible.
2. Preserve the original claim's scope, qualifications, uncertainty, causal direction, and point of view.
3. Make implicit structure explicit only when it is strongly entailed. Label any necessary interpretation as such.
4. Return the clearest faithful formulation, followed by a brief note about ambiguity only when one matters.

Prefer a compact paragraph. Use a structured form only when the object itself has several parts.

## Boundaries

- Do not strengthen, weaken, improve, critique, or defend the position.
- Do not replace the user's framing with a more fashionable or convenient one.
- Do not compress the broader conversation; that is SUMMARIZE.
- Do not extract lessons or conclusions; that is DISTILL.
- Perform this in the conversational agent; the exact local framing is the object, so an isolated worker adds no useful separation.
