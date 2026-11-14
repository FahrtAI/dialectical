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
Dialectical or run `/dialectical:dialectical`.

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
