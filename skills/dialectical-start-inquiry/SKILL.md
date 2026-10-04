---
name: dialectical-start-inquiry
description: Start a new Dialectical inquiry by creating its workspace and curating relevant context from prior inquiries and durable memory. Use when the user asks to begin, initialize, or branch an inquiry; do not imply that this creates a new chat in the surrounding platform.
---

# Start Inquiry

Create a clean conversational workspace without severing useful intellectual continuity.

Before acting, read [`../dialectical/references/memory.md`](../dialectical/references/memory.md) for the shared storage contract.

## Establish the inquiry

Infer a short working title and the new inquiry's initial focus from the request. Ask a question only when there is not enough information to identify the inquiry at all.

Treat “new” as a fresh inquiry context, not necessarily a wholly unrelated topic. Do not force the user to classify it before starting.

## Create the workspace

Use the current project or user-selected location as the workspace root. Initialize `.dialectical/` there when absent, then create:

```text
.dialectical/
├── .gitignore
├── manifest.yaml
├── conversations/
│   ├── index.md
│   └── YYYY-MM-DD-topic-slug/
│       ├── state.md
│       └── context.md
└── memory/
    ├── index.md
    └── objects/
```

Create the internal `.gitignore` specified by the storage contract so conversation data is private by default. Use a stable, filesystem-safe conversation ID. If the date and slug already exist, append a small numeric suffix rather than overwriting anything. Record the platform thread identifier when it is available, but do not require one.

`state.md` is the living state of this inquiry, not a transcript. Initialize it with metadata plus only the sections presently useful: focus, current understanding, findings, uncertainties, open questions, and saved objects.

`context.md` contains curated carryover from existing conversations and memory. Keep provenance links back to every source.

## Curate what already exists

1. Inventory existing entries in `.dialectical/conversations/` and `.dialectical/memory/objects/`.
2. Repair or create the two indexes from the files present. Never treat a missing index entry as permission to delete a file. Preserve a backup when replacing a materially divergent index.
3. Select prior material for relevance to the new inquiry, including useful disagreement, failed approaches, and unresolved questions.
4. Add a concise synthesis to the new `context.md` with source links and any important confidence or status markers.
5. Prefer links and distillation over copying whole records. Do not import unrelated history simply because it exists.
6. If an older conversation lacks a usable state record, derive only what its available material supports and mark the reconstruction as inferred.

Do not silently rewrite old conversation records during curation. Index repair and new cross-links are allowed; substantive changes to an old record require an explicit reason.

## Complete

Add the new conversation to `.dialectical/conversations/index.md` and report:

- the conversation ID and folder;
- the inferred focus;
- which prior conversations or memory objects were carried forward;
- whether the memory store was newly initialized.

Do not claim that a new platform chat was created, moved, or persisted unless the platform supports that operation and it actually occurred.
