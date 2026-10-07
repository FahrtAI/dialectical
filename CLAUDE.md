# Dialectical for Claude Code

Install or link every `skills/dialectical-*` directory, plus `skills/dialectical`, into a Claude Code skill discovery root such as `.claude/skills/` for a project or the corresponding user-level skills directory.

`CLAUDE.md` can state the governing principle—“formalize the interventions, not the conversation”—but a pointer in this file does not install or activate the standalone skills.

Invoke the Dialectical entry skill to apply its conversational discipline and optional checks. No always-loaded custom instructions are required for an explicitly invoked session.

After installation, verify that all skill names are discoverable and run the cases in `evals/cases.yaml` against each model intended for use.
