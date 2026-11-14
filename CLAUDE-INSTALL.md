# Dialectical in Claude

Dialectical installs as a Claude plugin from this repository, which is also its
plugin marketplace (`.claude-plugin/marketplace.json`, marketplace name
`fahrtai`). The same install works in Claude (web, desktop, Cowork) and Claude
Code.

## Install

**Claude:** Customize → Plugins → Add → Add marketplace → Add from a
repository → `FahrtAI/dialectical`, then add **Dialectical**.

**Claude Code:**

```sh
claude plugin marketplace add FahrtAI/dialectical
claude plugin install dialectical@fahrtai
```

On Claude Code 2.1.275 or later, `/plugin install dialectical --marketplace
FahrtAI/dialectical` does both in one step.

## Check the install

```sh
claude plugin details dialectical
```

The component inventory should list 20 skills, starting with `dialectical`, and
the version should match the latest release. In a session, ask Claude to use
Dialectical or run `/dialectical:start`.

## Commands

Each operation has a short command, defined in `.claude-plugin/plugin.json`:
`/dialectical:challenge`, `/dialectical:verify`, `/dialectical:distill`,
`/dialectical:save`, `/dialectical:guide`, and the rest of the help card in
lowercase with hyphens (`/dialectical:thought-experiment`). Text after the command
is what it applies to; with none, it applies to the current discussion.
`/dialectical:start`, `/dialectical:help`, and `/dialectical:join` open
Dialectical, show the help card, or join an existing conversation. The longer
skill names (`/dialectical:dialectical-challenge`) still work.

These commands exist only in the Claude plugin. They don't change the skills,
so the ChatGPT and Codex installs are unaffected.

## Update and remove

The plugin's version comes from `.claude-plugin/plugin.json`; installs stay on
that version until a release changes it. Update with
`claude plugin marketplace update fahrtai` and
`claude plugin update dialectical@fahrtai`, or from **Customize → Plugins** in
Claude. Remove with `claude plugin uninstall dialectical@fahrtai`.

## Without the marketplace

To try local changes, load the checkout directly:
`claude --plugin-dir /path/to/dialectical`.

After installing, run the scenarios in `QA/BEHAVIOR_CHECK.md` with each model
you intend to use.
