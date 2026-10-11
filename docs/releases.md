# Building and releasing Dialectical

Every push, pull request, or manually dispatched validation workflow runs the
source checks and harness tests, builds twice, compares the ZIP bytes, verifies
the archive against source, and uploads a downloadable CI artifact. These
checks exercise packaging and the evaluation harness, not installed ChatGPT.

## Local build

```sh
python3 scripts/package_plugin.py
```

The builder validates the package, all skill versions, current README/install
versions, QA version, and local skill links. It writes four files in `dist/`:

- `dialectical-VERSION.zip`: the installable skills-only package.
- `dialectical-VERSION.zip.sha256`: its checksum.
- `dialectical-VERSION.build.json`: source commit, dirty-state flag, release tag
  when supplied, and per-file hashes.
- `dialectical-VERSION.release.md`: release notes with installation and smoke-test links.

The same package bytes produce the same ZIP regardless of file timestamps,
permissions, input ordering, or compression-library version. ZIP entries use a
fixed timestamp and mode with no compression; the small Markdown/PNG package
does not need compression to justify introducing variation between machines.
The build record is separate so provenance does not change the plugin payload.
Dirty local builds are clearly labeled development builds.

To check an archive against the current source checkout:

```sh
python3 scripts/package_plugin.py --verify dist/dialectical-VERSION.zip
```

To verify a downloaded ZIP's checksum, run from its download directory:

```sh
shasum -a 256 -c dialectical-VERSION.zip.sha256
```

Checksums detect different bytes; they are not a signed attestation. Compare with
the checksum from the intended repository release or CI run.

## Tagged release

1. Choose a new version for changed plugin content. Update `plugin.json`, every
   skill's `metadata.version`, current version/archive references in `README.md`
   and `CHATGPT.md`, and `QA/cases/chatgpt.yaml`. Keep historical baseline records
   unchanged. Review other current-version documentation as appropriate.
2. Run the validation workflow's checks locally, commit the release source, and
   use a clean checkout. The release build rejects untracked changes, mismatched
   tag/version, tags pointing elsewhere, and uncommitted package inputs.
3. Create an annotated tag and verify it locally, substituting the actual version:

   ```sh
   git tag -a vVERSION -m "Dialectical VERSION"
   python3 scripts/package_plugin.py --release --tag vVERSION
   git push origin main
   git push origin vVERSION
   ```

4. The version tag runs the same validation/build job, then a release job
   downloads those exact tested artifacts and creates a **draft GitHub release**.
   Normal branch/PR builds cannot create a release. Only the release job has
   repository write permission; no extra credentials or runtime server are needed.
5. For a material skill-behavior release, run and review the focused
   `QA/cases/release.yaml` regression against the tagged source as described in
   [QA/RUNNING.md](../QA/RUNNING.md). Record failures, ungraded cases, missing
   telemetry, word-count tradeoffs, and the exact model configuration. This
   optional maintainer run does not establish installed-host acceptance.
6. Review the draft's version, commit, assets, and notes. Install the ZIP using
   [CHATGPT.md](../CHATGPT.md), perform the short smoke test in
   [QA/RELEASE_ACCEPTANCE.md](../QA/RELEASE_ACCEPTANCE.md), and record desktop and
   iPhone separately using
   [the reusable record](../QA/releases/TEMPLATE.md). Publish the draft when
   ready; state any failed, blocked, or untested surfaces.

An existing release is never overwritten by the workflow. If a rerun encounters
an existing draft, inspect it and its assets before deciding whether any repair
is needed. For a published release, use a new version/tag for changed content.
Do not move a published tag or replace its assets silently.

CI artifacts are retained for 30 days. Release attachments provide the durable
download after publication. A GitHub release does not update the user's account
plugin or prove host acceptance. See [#13](https://github.com/FahrtAI/dialectical/issues/13)
for the outstanding installed-host work.

Maintainer references: [GitHub workflow artifacts](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflow-artifacts)
and [GitHub CLI release creation](https://cli.github.com/manual/gh_release_create).
