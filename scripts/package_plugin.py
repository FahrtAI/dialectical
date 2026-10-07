#!/usr/bin/env python3
"""Build a skills-only ZIP. This is a maintainer utility, not a plugin runtime."""

from __future__ import annotations

import json
import zipfile

from validate_plugin_package import ROOT, package_files, validate
from validate_skills import main as validate_skills


def main() -> int:
    failures = validate()
    if validate_skills():
        failures.append("Skill validation failed")
    if failures:
        print("\n".join(failures))
        return 1
    version = json.loads((ROOT / "plugin.json").read_text())["version"]
    destination = ROOT / "dist" / f"dialectical-{version}.zip"
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in package_files():
            archive.write(path, path.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(destination) as archive:
        assert archive.testzip() is None
        assert set(archive.namelist()) == {
            path.relative_to(ROOT).as_posix() for path in package_files()
        }
    print(f"Created {destination.relative_to(ROOT)} (skills only)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
