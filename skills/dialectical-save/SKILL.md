---
name: dialectical-save
description: Persist a conversational object with enough meaning, provenance, and relationships to remain useful later. Use when the user wants to retain an idea, finding, question, connection, or other object; do not claim success unless durable storage actually occurred.
metadata:
  version: "0.6.1"
---

# Save

Preserve the selected idea or finding with its meaning, provenance, and uncertainty.

Without an authorized writable store, return a copyable Markdown record and say
it has not been saved outside this chat. Include only useful title, content,
context, source, relationships, and already established confidence. Do not save
the whole transcript or invent evidence. A prepared record is not a durable write.

When the user requests durable storage and an authorized filesystem is available,
read [the file procedure](references/file-storage.md) and the shared storage
contract linked there before writing. Resolve ambiguous destinations briefly.
Keep canonical and index writes in the conversational agent; confirm success only
after the write. Preserve the exact evidential scope, including source limitations,
of the original finding.
