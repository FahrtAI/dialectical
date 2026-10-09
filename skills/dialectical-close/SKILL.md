---
name: dialectical-close
description: Close or pause an active Dialectical inquiry by taking a final checkpoint and recording its status. Use only when the user asks to close, pause, finish, or archive the inquiry; do not end or archive the surrounding platform chat implicitly.
metadata:
  version: "0.6.1"
---

# Close Inquiry

Leave the inquiry recoverable without closing the platform chat.

Return a final checkpoint with the current assessment, evidence and its limits,
uncertainty, reversals, and open questions. Mark the inquiry paused or closed as
requested within the conversation; explain that the copyable note can be pasted
into another chat. Unresolved work stays unresolved. Do not claim a durable save.

For a user-authorized file store, read
[the file procedure](references/file-storage.md) and its shared storage contract
before taking the final checkpoint and changing status. Keep mutations in the
conversational agent. Never automatically delete, merge, or save other objects.
