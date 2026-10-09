# Optional filesystem procedure

Read this only when file access and the requested operation are authorized.
Follow the shared [storage contract](../../dialectical/references/memory.md).
Preserve the original scope and limitations of every finding when copying or updating it.

# Close Inquiry

Leave the inquiry recoverable and intellectually legible.

Read [`../../dialectical/references/memory.md`](../../dialectical/references/memory.md) before writing.

## Operation

Without an authorized writable file store, give a final checkpoint in chat,
retain unresolved questions, and mark the inquiry paused or closed within this
conversation. Tell the user they can paste that checkpoint into a later chat
to resume. Do not claim a durable write. The file procedure below is optional.

1. Resolve the current inquiry as CHECKPOINT does, and whether the requested status is `paused` or `closed`.
2. Perform a final checkpoint: current conclusion or state, supporting basis, unresolved uncertainty, open questions, and saved-object links.
3. Update `state.md` with the new status, timestamp, and a status-history entry, then update its index entry.
4. Identify any valuable unsaved findings, but do not save them automatically unless the request includes that authorization.
5. Confirm the inquiry record that was closed or paused and how it can be resumed.

## Boundaries

- Do not delete or merge the inquiry.
- Do not mark unresolved work complete merely because the conversation is ending.
- Do not archive or close the platform chat unless the user separately requests it and the platform supports it.
- Do not delegate the final checkpoint or status write; keep durable mutation in the conversational agent.
