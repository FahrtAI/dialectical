---
name: dialectical-save
description: Package the relevant conversation into a portable Markdown handoff that can be saved or imported into a new thread. Use for SAVE or requests to preserve and continue the conversation elsewhere; do not imply cross-chat memory or external storage.
metadata:
  version: "0.7.0"
---

# Save

Create a self-contained Markdown handoff that lets a fresh thread understand and
continue the inquiry.

Use the shortest complete surrounding chat response, but make the handoff as complete as
needed to preserve material evidence, provenance, disagreement, uncertainty,
and open questions. For a clear ordinary-language invocation that does not name
SAVE, begin with one line: `SAVE — <brief context-specific description>.` Omit
the cue for an explicit command or mere discussion. Exporting a claim does not
change its scope, confidence, or evidence status.

Save the whole relevant inquiry by default, not a verbatim transcript. If the
user explicitly names a branch, finding, or narrower span, save only that scope
with enough surrounding context to remain intelligible. Ask one brief question
only when the requested scope is materially ambiguous.

Use [the handoff format](references/handoff-format.md). Preserve the original
scope, provenance, disagreement, and uncertainty of every claim. Separate
supplied facts and sourced evidence from conversational hypotheses and analysis.
State important context that is missing or unavailable; do not reconstruct it.

When the host supports user-downloadable files, create a descriptively named
`.md` file and provide it. Otherwise, provide a filename and the complete,
copyable Markdown in the response, and say plainly that no file was created
outside the chat. Tell the user to save the document, then upload or paste it
into a new thread and ask Dialectical to continue from the handoff. The artifact
is portable user-owned context, not automatic cross-thread memory. Do not
require or invent an external service.

If the user explicitly requests a durable workspace copy, use the optional
[local file procedure](references/file-storage.md). This is secondary to
producing the portable handoff.

SAVE creates a transferable artifact. CHECKPOINT updates an inquiry's living
state; RECALL retrieves an existing record; RESUME continues from a supplied or
accessible record. Do not silently perform those operations or claim that a
handoff was stored, retrieved, or activated.
