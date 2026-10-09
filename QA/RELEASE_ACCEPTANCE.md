# Release acceptance record

Use one record per candidate package. Keep source, packaging, account update,
and installed-host evidence separate. A Git push does not update an account plugin.

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

For each device record app version, exact selected plugin/version, actual prompts,
responses, observed tools, and pass/fail/untested. Retain evidence sufficient to
reproduce a failure, excluding account secrets and unrelated conversation data.

| Check | Desktop | iPhone |
|---|---|---|
| Actual @ menu invocation and startup | untested | untested |
| Canonical help with GUIDE | untested | untested |
| GUIDE recommends without executing | untested | untested |
| Accept recommendation; only accepted scope executes | untested | untested |
| Decline; later turns do not repeat suggestion | untested | untested |
| CHECKPOINT → supplied note → RESUME with no store | untested | untested |
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
