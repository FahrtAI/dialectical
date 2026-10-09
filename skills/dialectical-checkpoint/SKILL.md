---
name: dialectical-checkpoint
description: Update the active Dialectical inquiry's living state without ending the conversation. Use when the user wants a durable checkpoint or before context may be lost; do not save the entire transcript by default.
metadata:
  version: "0.6.1"
---

# Checkpoint

Preserve the inquiry's intellectual state while leaving it open.

Normally return a compact copyable note: focus, findings with their evidence,
inferences, uncertainties, consequential reversals, and next questions. Do not
retell the transcript or claim it was saved elsewhere. Retain the original scope
and limitations of VERIFY verdicts, ACH rankings, and supplied records.

If the user requests a durable checkpoint in an authorized file store, read
[the file procedure](references/file-storage.md) and its shared storage contract.
Resolve the current inquiry from conversational context or a matching thread;
active status alone is insufficient. If ambiguous, ask which inquiry rather than
creating one. Keep state and index writes in the conversational agent.
