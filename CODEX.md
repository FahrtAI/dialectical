# Dialectical for Codex

Install or link every `skills/dialectical-*` directory, plus `skills/dialectical`, into a Codex skill discovery root such as `$CODEX_HOME/skills/`.

Keep the skills as sibling directories so each namespaced operation is independently discoverable. Project-scoped runtime state belongs in `.dialectical/`, not in the installed skill directories.

For the monitoring rules to run in ordinary conversation, add the lines from the README's "Always-on instructions" section to the project's `AGENTS.md`, or to `~/.codex/AGENTS.md`.

Validate the installed skills with the platform's skill validator and run `evals/cases.yaml` before treating the package as production-ready.
