---
name: dialectical-close
description: Close or pause an active Dialectical inquiry by taking a final checkpoint and recording its status. Use only when the user asks to close, pause, finish, or archive the inquiry; do not end or archive the surrounding platform chat implicitly.
metadata:
  version: "0.3.0"
---

# Close Inquiry

Leave the inquiry recoverable and intellectually legible.

Read [`../dialectical/references/memory.md`](../dialectical/references/memory.md) before writing.

## Operation

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
