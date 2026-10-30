---
name: dialectical-save
description: Package the relevant conversation into a portable Markdown handoff that can be saved or imported into a new thread, or export a cold read of one claim for an independent check in a fresh chat. Use for SAVE, requests to preserve and continue the conversation elsewhere, or requests to check a claim somewhere without this conversation's influence; do not imply cross-chat memory or external storage.
metadata:
  version: "0.8.0"
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
supplied facts and sourced evidence from conversational hypotheses and analysis,
and keep assistant-generated figures or claims labeled as such.
State important context that is missing or unavailable; do not reconstruct it.

## Cold read

When the user wants a claim checked independently, for example "SAVE cold
read," "give me something to check this in a fresh chat," or "let another model
look at this," export a cold read instead of a handoff, using
[the cold-read format](references/cold-read.md). A handoff carries the
conversation forward; a cold read deliberately leaves it behind. Every claim
arrives unverified, and the conversation's conclusions, trajectory, and the
user's preferred answer are left out.

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

SAVE creates a transferable artifact. With an authorized file store and an
explicit request, it can also save the current state into an active inquiry, as
the file procedure describes. RECALL retrieves an existing record; RESUME continues from a supplied or
accessible record. Do not silently perform those operations or claim that a
handoff was stored, retrieved, or activated.
