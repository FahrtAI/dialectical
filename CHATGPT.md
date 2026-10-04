# Dialectical for ChatGPT

The files in `skills/` are a canonical behavioral specification; ordinary ChatGPT and uploaded knowledge files do not execute this local skill collection or write `.dialectical/` storage.

A ChatGPT deployment needs a plugin, app, or API-backed integration that:

1. exposes each Dialectical operation;
2. supplies the active conversation focus;
3. implements authorized durable storage and retrieval;
4. preserves the memory trust boundary in `skills/dialectical/references/memory.md`.

Do not describe the repository alone as a turnkey ChatGPT integration. Static instructions can demonstrate the cognitive primitives, but SAVE, RECALL, and lifecycle operations require connected tools.
