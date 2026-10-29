---
name: dialectical-recap
description: Compress the relevant conversation or material into a shorter account of what was discussed. Use for RECAP, summarize requests, and context reduction; do not use to infer what was learned, evaluate claims, or reconstruct detailed provenance.
metadata:
  version: "0.8.0"
---

# Recap

Use the shortest complete response that preserves the speakers' actual scope,
qualifiers, disagreement, and uncertainty. For a clear ordinary-language
invocation that does not name RECAP, begin with one line:
`RECAP — <brief context-specific description>.` Omit the cue for explicit RECAP
or SUMMARIZE and for mere discussion. Compression does not create new findings
or change a claim's confidence.

Reduce the selected context while retaining the information needed to understand it.

RECAP is the command name. Accept SUMMARIZE and ordinary requests to summarize
as aliases for the same operation, not as a separate skill.

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
