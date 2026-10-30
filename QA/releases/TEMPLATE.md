# Dialectical release acceptance — VERSION

Allowed status values: `pass`, `fail`, `blocked`, `untested`.

## Candidate identity

| Field | Value |
|---|---|
| Version | |
| Commit | |
| Tag | |
| ZIP filename | |
| SHA-256 | |
| Build-record filename | |
| Account/workspace (non-sensitive) | |
| Tester and date | |

## Release stages

| Stage | Status | Evidence / limitation |
|---|---|---|
| Source committed and pushed | untested | |
| Tagged archive built and checksum verified | untested | |
| Automated source/package checks passed | untested | |
| Behavior check run (`QA/BEHAVIOR_CHECK.md`) | untested | |
| Account plugin installed or updated | untested | |
| Desktop accepted | untested | |
| iPhone accepted | untested | |
| Light/dark artwork inspected | untested | |
| GitHub release published | untested | |

## Environment

| Surface | ChatGPT/app version | OS/device | Installed plugin/version evidence |
|---|---|---|---|
| Desktop | | | |
| iPhone | | | |

## Installed-host results

| Check | Desktop status/evidence | iPhone status/evidence |
|---|---|---|
| Actual `@` invocation and START | untested | untested |
| HELP, FLOWS, and COOKBOOK | untested | untested |
| Natural-language cue and operation | untested | untested |
| GUIDE → selection and GUIDE → MORE | untested | untested |
| JOIN menu and selection boundary | untested | untested |
| Portable SAVE | untested | untested |
| Fresh-thread RESUME from supplied handoff | untested | untested |
| Ordinary conversation remains ordinary | untested | untested |
| Light-theme artwork | untested | untested |
| Dark-theme artwork | untested | untested |

## Behavior check

Model: ____ · Runs per cell: ____ · Share links: ____

| Scenario | A plain | B Dialectical | C paragraph (optional) |
|---|---|---|---|
| 1 Hold | untested | untested | untested |
| 2 Update | untested | untested | untested |
| 3 Own number | untested | untested | untested |
| 4 Consensus | untested | untested | untested |
| 5 No intervention | untested | untested | untested |

Reading (see `QA/BEHAVIOR_CHECK.md`):

## Failures and follow-up

Link each defect to its owning issue. Do not repair unrelated product behavior
inside this record. If packaged content changes, build a new candidate and
repeat the affected checks.

## Acceptance statement

State exactly which surfaces passed and which remain failed, blocked, or
untested. A source push, local validation, API evaluation, or model self-report
does not establish installed-host acceptance.
