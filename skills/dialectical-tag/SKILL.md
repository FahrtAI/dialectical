---
name: dialectical-tag
description: Attach concise structured metadata to a conversational object so it can be classified, related, and retrieved. Use for organizing an idea, claim, question, hypothesis, finding, or saved object; do not use to persist the object itself.
metadata:
  version: "0.2.0"
---

# Tag

Describe a conversational object with the smallest useful set of structured metadata.

When applying metadata to an already saved Dialectical object, read [`../dialectical/references/memory.md`](../dialectical/references/memory.md), preserve its identifier and provenance, and confirm the durable update.

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
6. Apply the metadata when the environment supports it; otherwise return a compact proposed metadata record. TAG does not create a new durable object, but it may update an object that SAVE already persisted.

## Boundaries

- Do not require every candidate field.
- Do not let metadata replace the object's actual content.
- Do not create a large taxonomy to tag a single object.
- Do not claim that an unsaved conversational object became durable; that is SAVE.
- Handle the tagging decision in the conversational agent; an isolated worker adds no useful separation for this small contextual operation.
- Do not delegate an update to a saved object's metadata; keep durable mutations in the conversational agent.
