#!/usr/bin/env python3
"""Build a development or public plugin ZIP after the appropriate preflight."""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path

from validate_plugin_package import ROOT, validate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--development",
        action="store_true",
        help="Allow the local MCP URL and omit production-only URL requirements.",
    )
    args = parser.parse_args()
    production = not args.development
    failures = validate(production=production)
    if failures:
        mode = "Production" if production else "Development"
        print(f"{mode} package not created:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    version = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))["version"]
    suffix = "" if production else "-dev"
    destination = ROOT / "dist" / f"dialectical-{version}{suffix}.zip"
    destination.parent.mkdir(parents=True, exist_ok=True)
    roots = [
        ROOT / "plugin.json",
        ROOT / "mcp.json",
        ROOT / ".codex-plugin",
        ROOT / ".mcp.json",
        ROOT / "skills",
    ]
    if (ROOT / "assets").exists():
        roots.append(ROOT / "assets")

    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for source in roots:
            files = [source] if source.is_file() else sorted(source.rglob("*"))
            for path in files:
                if path.is_file():
                    archive.write(path, path.relative_to(ROOT).as_posix())

    print(f"Created {destination.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
