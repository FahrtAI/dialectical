# Dialectical for Gemini CLI

Gemini CLI discovers workspace skills from `.gemini/skills/` or `.agents/skills/`, and user skills from the corresponding directories in the user profile.

Link or copy every `skills/dialectical-*` directory, plus `skills/dialectical`, into one of those discovery roots. During development, link each skill explicitly and reload the skill catalog.

Invoke the Dialectical entry skill after installing it. A pointer in a platform instruction file does not install skills. Verify discovery; file persistence is an optional host capability.
