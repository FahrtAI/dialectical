# Dialectical for Codex

Install or link every `skills/dialectical-*` directory, plus `skills/dialectical`, into a Codex skill discovery root such as `$CODEX_HOME/skills/`.

Keep the skills as sibling directories so each namespaced operation is independently discoverable. Project-scoped runtime state belongs in `.dialectical/`, not in the installed skill directories.

Invoke the Dialectical entry skill to apply its conversational discipline and optional checks. File persistence is optional and requires authorized filesystem access.

Validate the installed skills with the platform's skill validator and run the scenarios in `QA/BEHAVIOR_CHECK.md` before treating the package as production-ready.
