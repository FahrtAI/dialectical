# Dialectical 0.6.1 candidate acceptance

Recorded October 9, 2026. Implementation starts from commit `627e65e`; source
changes and this record are included together in the remediation commit.

| Stage | Recorded result |
|---|---|
| Skill layout, references, help, release versions | 24 skills pass local validation |
| Manifest and assets | Local package validator passes |
| Case definitions | 148 parsed and checked; 56 deferred for missing fixture/provider/host requirements |
| Complete smoke inputs | 12 cases, all prerequisites supplied |
| Harness tests | 19 pass; these use test doubles, not model evaluation |
| Behavioral pilot | Eight cases × three conditions; independent transcript grading passes, with limits in baseline README |
| Optional file memory | One independently executed compatibility scenario reviewed; see memory-review.md |
| ZIP | `dist/dialectical-0.6.1.zip`, skills only |
| ZIP SHA-256 | `bd344402ea1979fb7a60c283c7e1bd57fbc36c52b860b592bba4c03f22ad70b0` |
| Account plugin update | Not performed by this source change |
| Desktop acceptance | Untested |
| iPhone acceptance | Untested |
| Actual host light/dark logo rendering | Untested |

The PNG alpha-channel inspection disproved the earlier blank-square diagnosis.
No artwork was changed based on that diagnosis. Actual host rendering remains
part of issue #13 and must use the record in `QA/RELEASE_ACCEPTANCE.md`.

A read-only Codex CLI connectivity probe returned READY. CLI 0.132.0 also logged
a model-catalog parsing incompatibility and loaded installed plugin context, so
that probe was not treated as an isolated comparative evaluation or a host pass.
No CLI upgrade or account-plugin change was performed as part of this work.

Future complete-suite work stays in #4; stronger comparative measurement in #11;
device/account acceptance in #13. Do not close tracker #14 from local checks.
