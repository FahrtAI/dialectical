# Dialectical for Codex

Install or link every `skills/dialectical-*` directory, plus `skills/dialectical`, into a Codex skill discovery root such as `$CODEX_HOME/skills/`.

Keep the skills as sibling directories so each namespaced operation is independently discoverable. Project-scoped runtime state belongs in `.dialectical/`, not in the installed skill directories.

Validate the installed skills with the platform's skill validator and run `evals/cases.yaml` before treating the package as production-ready.
