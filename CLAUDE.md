# Dialectical for Claude Code

Install or link every `skills/dialectical-*` directory, plus `skills/dialectical`, into a Claude Code skill discovery root such as `.claude/skills/` for a project or the corresponding user-level skills directory.

`CLAUDE.md` can state the governing principle—“formalize the interventions, not the conversation”—but a pointer in this file does not install or activate the standalone skills.

For the monitoring rules to run in ordinary conversation, add the lines from the README's "Always-on instructions" section to the `CLAUDE.md` of each project where you use Dialectical, or to `~/.claude/CLAUDE.md`.

After installation, verify that all skill names are discoverable and run the cases in `evals/cases.yaml` against each model intended for use.
