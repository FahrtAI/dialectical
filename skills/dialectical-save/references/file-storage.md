# Optional local file procedure

Use this only when the user explicitly requests a workspace copy and file access
is authorized. The portable Markdown handoff remains the primary SAVE result.

1. Generate the complete handoff using [the handoff format](handoff-format.md).
2. Use a descriptive, filesystem-safe `.md` filename in the destination the
   user names, or the current working folder if they name none.
3. Avoid overwriting an existing export unless the user clearly requested it.
4. Re-read the written file and report its path only after a successful write.

Do not create a memory index or imply that the local file will be visible in
another chat. The user must attach or paste the handoff there.
