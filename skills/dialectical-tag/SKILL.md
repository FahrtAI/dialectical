---
name: dialectical-tag
description: Attach concise structured metadata to a conversational object so it can be classified, related, and retrieved. Use for organizing an idea, claim, question, hypothesis, finding, or saved object; do not use to persist the object itself.
metadata:
  version: "0.8.0"
---

# Tag

Apply the smallest useful metadata to the selected object.

Use the shortest complete response that preserves the object's content,
identity, provenance, and evidence status. For a clear ordinary-language
invocation that does not name TAG, begin with one line:
`TAG — <brief context-specific description>.` Omit the cue for an explicit
command or mere discussion. Metadata such as `finding`, `confirmed`, or a
confidence label must not upgrade what the evidence warrants.

Preserve its content and identity. Use concise reusable terms for relevant type,
domain, concepts, mechanism, status, relationships, or provenance. Distinguish
supplied metadata from inference; do not invent confidence or origin. Do not
require every field or build a taxonomy for one idea.

Normally return proposed metadata in chat; TAG does not create a durable object.
When updating an already saved object in an authorized file store, read
[the file procedure](references/file-storage.md) and its shared storage contract.
Preserve identifiers and provenance, write in the conversational agent, and claim
an update only when it actually occurred.
