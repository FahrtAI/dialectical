# Optional local file procedure

Use this only when the user explicitly requests a workspace copy and file access
is authorized. The portable Markdown handoff remains the primary SAVE result.

1. Generate the complete handoff using [the handoff format](handoff-format.md).
2. Use a descriptive, filesystem-safe `.md` filename. Prefer
   `.dialectical/exports/` when an existing Dialectical workspace is in use;
   otherwise use the user-specified destination.
3. Avoid overwriting an existing export unless the user clearly requested it.
4. Re-read the written file and report its path only after a successful write.

Do not create a memory index or imply that the local file will be visible in
another chat. The user must attach or paste the handoff there.

## Save into an active inquiry

Only when the user explicitly asks to save into, or update, an inquiry in an
authorized store. Read the shared
[storage contract](../../dialectical/references/memory.md) first. This replaces
the former CHECKPOINT operation: a distillation is the checkpoint, and this
step persists it.

1. Resolve the current inquiry: the one this conversation started or resumed,
   or the one whose `thread_id` matches. Status alone does not identify it. If
   it cannot be identified, list active inquiries and ask, or offer START
   INQUIRY. Never create one silently.
2. Distill the present focus, findings with their status and origin,
   uncertainties, open questions, consequential pivots, and saved-object links.
3. Merge that state into the inquiry's `state.md`. Preserve earlier material
   that still explains provenance; record superseded conclusions rather than
   erasing them.
4. Update the inquiry metadata and index only after `state.md` is safely written.
5. Report what materially changed since the previous saved state.

Keep these writes in the conversational agent. Do not convert tentative ideas
into findings.
