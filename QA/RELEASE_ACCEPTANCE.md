# Release acceptance record

Use one record per candidate package. Keep source, packaging, account update,
and installed-host evidence separate. A Git push does not update an account plugin.

Use exactly `pass`, `fail`, `blocked`, or `untested` for each check. `blocked`
means the check was attempted but an identified account, device, surface, or
host capability prevented it; `untested` means it was not attempted. Neither is
a pass. Copy [`releases/TEMPLATE.md`](releases/TEMPLATE.md) for each candidate
and retain the completed record with the release evidence.

## Short post-install smoke test

Run this on desktop and iPhone separately after updating the account plugin.
Use a fresh chat on each device and record the actual responses.

1. Take the expected version, commit, and ZIP checksum from the release's
   `.build.json` attachment. Check the downloaded ZIP against `.zip.sha256` and
   record which package was used for the account update.
2. If the host exposes installed version metadata, compare it with the release.
   Otherwise record version verification as unconfirmed. You may ask Dialectical
   to read its loaded entry skill's `metadata.version`; record that as a reported
   version only. Model self-report alone does not prove the installed package.
3. Select the actual Dialectical entry from the `@` menu and send
   `@Dialectical start a conversation`. Expect a short opening question, with no
   server or storage setup. Supply a topic and confirm it continues normally.
4. Ask `@Dialectical help`. Expect the canonical ASCII card. For a candidate
   containing in-chat references, ask `flows` and `cookbook` separately. Confirm
   that each reference is shown without research, saving, or other operations
   starting automatically.
5. After a few turns, ask `Catch me up on what we discussed`. Expect one brief
   `RECAP` cue followed by a faithful recap, with no confirmation step or method
   lecture.
6. Ask `SAVE this conversation so I can continue it in a new thread` and verify
   a downloadable `.md` handoff or complete copyable Markdown fallback.
   If the fallback is used, expect an honest statement that no file was created;
   if a file is provided, verify that it contains the complete handoff.
7. Open a fresh thread, supply the produced file or complete copied Markdown,
   and ask `@Dialectical RESUME from this handoff`. Confirm that it reconstructs
   only the supplied qualified state, does not claim access to the original
   thread, and can continue from a new user update.

Record pass/fail/untested and version-confirmation limitations below. This short
test does not replace the GUIDE/continuity or light/dark checks in the full matrix.
Copy this template into a separate candidate record; leave this template reusable.

## Candidate record

| Field | Value |
|---|---|
| Candidate version | |
| Commit / dirty state | |
| Archive path and SHA-256 | |
| Source validation results | |
| Harness / behavioral results and limitations | |
| Account plugin version actually installed | |
| Account/workspace identifier (non-sensitive) | |
| Tester and date | |

Record release stages independently:

| Stage | Status | Evidence / limitation |
|---|---|---|
| Source committed and pushed | untested | |
| Tagged archive built and checksum verified | untested | |
| Automated source/package checks passed | untested | |
| Focused behavioral regression reviewed | untested | |
| Account plugin installed or updated | untested | |
| Desktop accepted | untested | |
| iPhone accepted | untested | |
| Light/dark artwork inspected | untested | |
| GitHub release published | untested | |

For each device record app version, OS/device, exact selected plugin/version,
actual prompts, responses, observed tools, and status. Retain evidence sufficient to
reproduce a failure, excluding account secrets and unrelated conversation data.

| Check | Desktop | iPhone |
|---|---|---|
| Actual @ menu invocation and startup | untested | untested |
| Canonical help with GUIDE | untested | untested |
| HELP retrieves both FLOWS and COOKBOOK | untested | untested |
| Natural-language RECAP uses one brief cue | untested | untested |
| GUIDE ranks three, MORE shows all, selection runs one | untested | untested |
| JOIN offers RECAP / DISTILL / TRACE / CONTINUE | untested | untested |
| SAVE produces a portable Markdown handoff | untested | untested |
| Fresh thread resumes from supplied handoff | untested | untested |
| Select ranked GUIDE choice; only that command executes | untested | untested |
| Ignore GUIDE menu; ordinary conversation continues | untested | untested |
| SAVE → supplied handoff → RESUME with no store | untested | untested |
| Composer/listing icon, light theme | untested | untested |
| Composer/listing icon, dark theme | untested | untested |

Logo checks: inspect transparency against the actual host background, recognizability
at display size, clipping, and dark-theme contrast. The packaged monochrome PNGs
contain the symbol in their alpha channel; a viewer showing only uniform RGB
does not establish that they are blank. Change artwork only for reproduced defects.

Keep [issue #13](https://github.com/FahrtAI/dialectical/issues/13) open until both
device outcomes are recorded, or explicitly document unsupported/unavailable
surfaces as unresolved. Optional adapters, local evaluations, and file-storage
checks do not substitute for these tests.
