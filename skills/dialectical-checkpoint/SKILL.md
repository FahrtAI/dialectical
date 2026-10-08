---
name: dialectical-checkpoint
description: Update the active Dialectical inquiry's living state without ending the conversation. Use when the user wants a durable checkpoint or before context may be lost; do not save the entire transcript by default.
metadata:
  version: "0.6.0"
---

# Checkpoint

Preserve the current intellectual state while leaving the inquiry open.

Read [`../dialectical/references/memory.md`](../dialectical/references/memory.md) before writing.

## Operation

Without an authorized writable file store, return a compact checkpoint in
chat: focus, findings and their basis, uncertainty, reversals, and next questions.
Say it is a copyable note, not a separately saved record, and leave the inquiry
open. The file procedure below applies only when storage is available.

1. Resolve the current inquiry: the one this conversation started or resumed, or the one whose `thread_id` matches. Status alone does not identify it, because several inquiries may be active.
2. Distill the present focus, established findings, inferences, uncertainties, open questions, consequential pivots, and saved-object links.
3. Merge that state into the inquiry's `state.md`. Preserve earlier material that still explains provenance; record superseded conclusions rather than silently erasing them.
4. Update the inquiry metadata and conversations index only after the state file is safely written.
5. Report what materially changed.

If the current inquiry cannot be identified, list the active inquiries and ask which one, or offer START INQUIRY. Do not create a new inquiry silently.

## Boundaries

- Do not turn checkpointing into a mandatory cadence.
- Do not convert tentative ideas into findings.
- Do not claim that the platform transcript itself was saved.
- Do not delegate state or index writes; keep the checkpoint mutation in the conversational agent.
