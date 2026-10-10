#!/usr/bin/env python3
"""Build a skills-only ZIP. This is a maintainer utility, not a plugin runtime."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import subprocess
import zipfile
from pathlib import Path

from validate_plugin_package import ROOT, package_files, validate
from validate_skills import main as validate_skills


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True).strip()


def source_state() -> dict:
    return {"commit": git("rev-parse", "HEAD"),
            "dirty": bool(git("status", "--porcelain", "--untracked-files=all"))}


def check_release(version: str, tag: str | None, state: dict, files: list[Path]) -> None:
    if state["dirty"]:
        raise ValueError("Release builds require a clean checkout (including untracked files).")
    if tag != f"v{version}":
        raise ValueError(f"Release tag must be v{version}, matching plugin.json.")
    if git("rev-parse", "--verify", f"refs/tags/{tag}^{{commit}}") != state["commit"]:
        raise ValueError("Release tag must point to the checked-out commit.")
    tracked = set(git("ls-files", "-z").split("\0"))
    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        if relative not in tracked:
            raise ValueError(f"Untracked or ignored package input: {relative}")
        committed = subprocess.check_output(
            ["git", "-C", str(ROOT), "show", f"HEAD:{relative}"])
        if path.read_bytes() != committed:
            raise ValueError(f"Package input differs from committed bytes: {relative}")


def package_inputs(files: list[Path]) -> dict[str, bytes]:
    inputs = {}
    for path in files:
        if path.is_symlink() or not path.resolve().is_relative_to(ROOT.resolve()):
            raise ValueError(f"Unsafe package input: {path}")
        inputs[path.relative_to(ROOT).as_posix()] = path.read_bytes()
    return inputs


def archive_bytes(inputs: dict[str, bytes]) -> bytes:
    """Stable ordering, timestamps and modes; no platform-dependent compression."""
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as archive:
        for name, content in sorted(inputs.items()):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content)
    return output.getvalue()


def verify_archive(data: bytes, inputs: dict[str, bytes]) -> None:
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)) or set(names) != set(inputs):
            raise ValueError("Archive has missing, extra, or duplicate paths.")
        if archive.testzip() is not None:
            raise ValueError("Archive CRC validation failed.")
        for name, content in inputs.items():
            if archive.read(name) != content:
                raise ValueError(f"Archive content differs from source: {name}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release", action="store_true", help="Require a clean, tagged commit")
    parser.add_argument("--tag", help="Exact release tag, v<plugin version>")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist")
    parser.add_argument("--verify", type=Path, help="Check an existing ZIP against this source")
    args = parser.parse_args(argv)
    if args.tag and not args.release:
        parser.error("--tag requires --release")
    failures = validate()
    if validate_skills():
        failures.append("Skill validation failed")
    if failures:
        print("\n".join(failures))
        return 1
    version = json.loads((ROOT / "plugin.json").read_text())["version"]
    try:
        files = package_files()
        state = source_state()
        if args.release:
            check_release(version, args.tag, state, files)
        inputs = package_inputs(files)
        if args.verify:
            verify_archive(args.verify.read_bytes(), inputs)
            print(f"Verified archive paths and bytes against source: {args.verify}")
            return 0
        data = archive_bytes(inputs)
        verify_archive(data, inputs)
        digest = hashlib.sha256(data).hexdigest()
        destination = args.output_dir / f"dialectical-{version}.zip"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        destination.with_suffix(".zip.sha256").write_text(
            f"{digest}  {destination.name}\n", encoding="utf-8")
        record = {
            "version": version, "tag": args.tag, "source": state,
            "release_candidate": args.release, "archive": destination.name,
            "sha256": digest,
            "files": {name: hashlib.sha256(content).hexdigest()
                      for name, content in sorted(inputs.items())},
            "host_acceptance": "untested",
        }
        destination.with_suffix(".build.json").write_text(
            json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        destination.with_suffix(".release.md").write_text(
            f"# Dialectical {version}\n\n"
            f"Source commit: `{state['commit']}`. Dirty checkout: `{state['dirty']}`.\n\n"
            f"Archive: `{destination.name}`\n\nSHA-256: `{digest}`\n\n"
            "See the attached build record for per-file hashes. Only the plugin ZIP "
            "is installed; the other attachments are build evidence.\n\n"
            "Account installation, desktop/iPhone behavior, and light/dark artwork "
            "are **untested** until separately recorded. A GitHub release does not "
            "update an installed ChatGPT plugin.\n\n"
            f"[Install/update instructions](https://github.com/FahrtAI/dialectical/blob/{state['commit']}/CHATGPT.md) · "
            f"[Post-install smoke test](https://github.com/FahrtAI/dialectical/blob/{state['commit']}/QA/RELEASE_ACCEPTANCE.md)\n",
            encoding="utf-8")
    except (ValueError, OSError, subprocess.CalledProcessError, zipfile.BadZipFile) as error:
        print(f"Build failed: {error}")
        return 1
    print(f"Created {destination} (skills only); SHA-256 {digest}")
    if state["dirty"]:
        print("Development build: source has uncommitted changes; not a release candidate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
