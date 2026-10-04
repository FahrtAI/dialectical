---
name: dialectical-checkpoint
description: Update the active Dialectical inquiry's living state without ending the conversation. Use when the user wants a durable checkpoint or before context may be lost; do not save the entire transcript by default.
---

# Checkpoint

Preserve the current intellectual state while leaving the inquiry open.

Read [`../dialectical/references/memory.md`](../dialectical/references/memory.md) before writing.

## Operation

1. Resolve the active inquiry from context or its platform thread identifier.
2. Distill the present focus, established findings, inferences, uncertainties, open questions, consequential pivots, and saved-object links.
3. Merge that state into the inquiry's `state.md`. Preserve earlier material that still explains provenance; record superseded conclusions rather than silently erasing them.
4. Update the inquiry metadata and conversations index only after the state file is safely written.
5. Report what materially changed.

If no active inquiry can be identified, ask for its identifier or offer START INQUIRY. Do not create a new inquiry silently.

## Boundaries

- Do not turn checkpointing into a mandatory cadence.
- Do not convert tentative ideas into findings.
- Do not claim that the platform transcript itself was saved.
