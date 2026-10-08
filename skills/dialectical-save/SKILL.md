---
name: dialectical-save
description: Persist a conversational object with enough meaning, provenance, and relationships to remain useful later. Use when the user wants to retain an idea, finding, question, connection, or other object; do not claim success unless durable storage actually occurred.
metadata:
  version: "0.6.0"
---

# Save

Preserve the selected object as durable knowledge rather than an isolated transcript fragment.

Read [`../dialectical/references/memory.md`](../dialectical/references/memory.md). Without an authorized writable file store, return the selected content as a copyable Markdown record with provenance and uncertainty, and state that it has not been saved outside this chat. Skip storage operations; do not ask the user to deploy or connect a service. Skill instructions and chat history alone are not a plugin-owned durable store.

## Operation

1. Resolve exactly what the user wants retained. Include multiple objects only when their relationship is the object of interest.
2. Preserve the object's substantive content and add only the context needed to understand why it matters later.
3. When supported, record:
   - a concise title or identifier;
   - content;
   - object type and status;
   - relevant context;
   - provenance;
   - relationships to other objects;
   - confidence or uncertainty when already established;
   - creation or update time.
4. Reuse TAG-compatible metadata when it improves retrieval, but do not force a complete schema.
5. Persist to the available user-authorized store. Prefer the current workspace's `.dialectical/memory/objects/` when it exists or the inquiry was initialized by START INQUIRY. Create a missing Dialectical store when the user invoked SAVE in a local workspace and no competing destination is implied. If several materially different destinations are possible, ask one brief question rather than guessing.
6. Write the object before rebuilding `memory/index.md`; do not leave an index pointing to a missing object. If updating an existing object, preserve its identifier and record what it supersedes or changes.
7. Link the object from the active conversation's `state.md` when one is known.
8. Confirm what was saved and provide its identifier or location. If durable storage is unavailable, return a ready-to-save record and explicitly say it was not persisted.

## Boundaries

- Do not save the entire surrounding conversation by default.
- Do not silently alter the substance to make the record neater.
- Do not invent provenance, relationships, or confidence.
- Do not claim an in-chat rendering is durable storage.
- Do not delegate canonical or index writes; keep durable mutations in the conversational agent.
