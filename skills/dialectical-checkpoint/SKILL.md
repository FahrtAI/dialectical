---
name: dialectical-checkpoint
description: Update the active Dialectical inquiry's living state without ending the conversation. Use when the user wants a durable checkpoint or before context may be lost; do not save the entire transcript by default.
metadata:
  version: "0.7.0"
---

# Checkpoint

Preserve the inquiry's intellectual state while leaving it open.

Use the shortest complete response that preserves material evidence,
provenance, reversals, disagreement, and uncertainty. For a clear
ordinary-language invocation that does not name CHECKPOINT, begin with one line:
`CHECKPOINT — <brief context-specific description>.` Omit the cue for an
explicit command or mere discussion. Change a claim's scope or confidence only
when the stated evidence or analysis justifies it.

Normally return a compact copyable note: focus, findings with their evidence,
inferences, uncertainties, consequential reversals, and next questions. Do not
retell the transcript or claim it was saved elsewhere. Retain the original scope
and limitations of VERIFY verdicts, ACH rankings, and supplied records.

If the user requests a durable checkpoint in an authorized file store, read
[the file procedure](references/file-storage.md) and its shared storage contract.
Resolve the current inquiry from conversational context or a matching thread;
active status alone is insufficient. If ambiguous, ask which inquiry rather than
creating one. Keep state and index writes in the conversational agent.
