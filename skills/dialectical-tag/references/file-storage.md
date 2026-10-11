# Optional filesystem procedure

Read this only when file access and the requested operation are authorized.
Follow the shared [storage contract](../../dialectical/references/memory.md).
Preserve the original scope and limitations of every finding when copying or updating it.

# Tag

Describe a conversational object with the smallest useful set of structured metadata.

When applying metadata to an already saved Dialectical object, read [`../../dialectical/references/memory.md`](../../dialectical/references/memory.md) and preserve its identifier and provenance. Confirm an update only when it was actually written; otherwise return proposed metadata in chat.

## Operation

1. Resolve the object being tagged and preserve its identity separately from its metadata.
2. Use only fields that improve classification, association, or retrieval. Candidate fields include:
   - `type`
   - `domain`
   - `concepts`
   - `mechanism`
   - `status`
   - `confidence`
   - `relationships`
   - `provenance`
3. Prefer normalized, reusable terms over sentence-length labels or near-duplicates.
4. Represent relationships explicitly when useful, including the related object and relation type.
5. Distinguish supplied metadata from inferred metadata. Do not invent provenance or confidence.
6. Apply the metadata when an existing durable object and an authorized storage environment support it; otherwise return a compact proposed metadata record. TAG does not create a new durable object. A portable SAVE handoff is a document, not a memory object; tag it only as an explicitly selected document or record.

## Boundaries

- Do not require every candidate field.
- Do not let metadata replace the object's actual content.
- Do not create a large taxonomy to tag a single object.
- Do not claim that an unsaved conversational object became durable. SAVE can export a portable handoff, but it does not create or update a memory object.
- Handle the tagging decision in the conversational agent; an isolated worker adds no useful separation for this small contextual operation.
- Do not delegate an update to a saved object's metadata; keep durable mutations in the conversational agent.
