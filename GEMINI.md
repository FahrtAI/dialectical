# Dialectical for Gemini CLI

Gemini CLI discovers workspace skills from `.gemini/skills/` or `.agents/skills/`, and user skills from the corresponding directories in the user profile.

Link or copy every `skills/dialectical-*` directory, plus `skills/dialectical`, into one of those discovery roots. During development, link each skill explicitly and reload the skill catalog.

`GEMINI.md` may carry the governing conversational principle, but it does not replace skill installation. For the monitoring rules to run in ordinary conversation, add the lines from the README's "Always-on instructions" section to the project's `GEMINI.md`, or to `~/.gemini/GEMINI.md`. Verify discovery before relying on routing or memory operations.
