---
name: dialectical-summarize
description: Compress the relevant conversation or material into a shorter account of what was discussed. Use for recap and context reduction; do not use to infer what was learned, evaluate claims, or reconstruct detailed provenance.
metadata:
  version: "0.1.0"
---

# Summarize

Reduce the selected context while retaining the information needed to understand it.

## Operation

1. Infer the intended span: the current exchange, a named branch, supplied material, or the conversation so far.
2. Identify the main topics, positions, developments, and unresolved items in that span.
3. Compress repetition and examples unless an example carries essential meaning.
4. Preserve disagreement and uncertainty rather than blending them into consensus.
5. Organize chronologically or thematically, whichever makes the recap easier to recover from.

Scale length to the source and the user's purpose. A summary reports what was discussed; it does not claim that the discussion established it.

## Boundaries

- Do not introduce new conclusions.
- Do not turn the recap into a critique or research report.
- Do not emphasize the path of pivots and influences unless requested; that is TRACE.
- Do not substitute extracted findings for conversational coverage; that is DISTILL.
- Perform this in the conversational agent; the selected conversation is the source material, so an isolated worker adds no useful separation.
