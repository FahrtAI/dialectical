# Dialectical for Gemini CLI

Gemini CLI discovers workspace skills from `.gemini/skills/` or `.agents/skills/`, and user skills from the corresponding directories in the user profile.

Link or copy every `skills/dialectical-*` directory, plus `skills/dialectical`, into one of those discovery roots. During development, link each skill explicitly and reload the skill catalog.

`GEMINI.md` may carry the governing conversational principle, but it does not replace skill installation. Verify discovery before relying on routing or memory operations.
