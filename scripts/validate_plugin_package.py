#!/usr/bin/env python3
"""Check this skills-only package against documented portable/OpenAI constraints.

Source: https://developers.openai.com/plugins/build/plugins
Metadata: https://developers.openai.com/plugins/deploy/submission
These local checks do not replace OpenAI's upload scans or installed-host tests.
"""

from __future__ import annotations

import json
import re
import struct
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"


def package_files() -> list[Path]:
    manifest = json.loads((ROOT / "plugin.json").read_text())
    interface = manifest["extensions"]["com.openai"]["interface"]
    files = [ROOT / "plugin.json"]
    files.extend(sorted((ROOT / "skills").rglob("*.md")))
    for key in ("logo", "logoDark", "composerIcon", "composerIconDark"):
        if key in interface:
            files.append(ROOT / interface[key])
    return sorted(set(files))


def validate() -> list[str]:
    failures = []
    try:
        manifest = json.loads((ROOT / "plugin.json").read_text())
        if not isinstance(manifest, dict):
            return ["plugin.json must contain an object"]
    except (OSError, ValueError) as error:
        return [f"Cannot read plugin.json: {error}"]
    allowed = {"$schema", "name", "version", "description", "author",
               "homepage", "repository", "license", "keywords", "extensions"}
    if set(manifest) - allowed:
        failures.append("Unsupported portable manifest fields")
    if manifest.get("$schema") != SCHEMA:
        failures.append("Missing portable Agent Plugins 1.0 schema")
    if manifest.get("name") != "dialectical":
        failures.append("Plugin identity must remain dialectical")
    if not re.fullmatch(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)",
                        str(manifest.get("version", ""))):
        failures.append("Release version must be semver")
    if not isinstance(manifest.get("description"), str) or not 1 <= len(manifest["description"]) <= 4000:
        failures.append("Description must contain 1–4000 characters")
    for path in ("mcp.json", ".mcp.json", ".app.json", "hooks", "server",
                 ".codex-plugin/plugin.json"):
        if (ROOT / path).exists():
            failures.append(f"Unnecessary infrastructure remains: {path}")
    extension = manifest.get("extensions", {}).get("com.openai", {})
    if not isinstance(extension, dict) or set(extension) - {"interface"}:
        return failures + ["This package needs only the OpenAI interface extension"]
    interface = extension.get("interface", {})
    if not isinstance(interface, dict):
        return failures + ["interface must be an object"]
    limits = {"displayName": 30, "shortDescription": 30,
              "longDescription": 4000, "developerName": 80}
    for key, limit in limits.items():
        value = interface.get(key)
        if not isinstance(value, str) or not value.strip() or len(value) > limit:
            failures.append(f"Invalid interface.{key}")
    if interface.get("displayName") != "Dialectical":
        failures.append("Display name must be Dialectical")
    if interface.get("category") != "Education & Research":
        failures.append("Unexpected listing category")
    capabilities = interface.get("capabilities", [])
    if not isinstance(capabilities, list) or len(capabilities) > 20 or any(
        not isinstance(item, str) or not item.strip() or len(item) > 120
        for item in capabilities
    ):
        failures.append("Invalid capabilities")
    prompts = interface.get("defaultPrompt", [])
    if isinstance(prompts, str):
        prompts = [prompts]
    if not isinstance(prompts, list) or len(prompts) > 3 or any(
        not isinstance(p, str) or not p.strip() or len(p) > 128 or "@" in p
        for p in prompts
    ):
        failures.append("Invalid starter prompts")
    elif len(set(prompts)) != len(prompts):
        failures.append("Starter prompts must be unique")
    for key in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
        if key in interface:
            url = urlparse(interface[key])
            if url.scheme != "https" or not url.netloc or url.username or url.password or len(interface[key]) > 1024:
                failures.append(f"Invalid interface.{key}")
    for key in ("logo", "logoDark", "composerIcon", "composerIconDark"):
        value = interface.get(key)
        if value is None:
            continue
        if not isinstance(value, str) or not value.startswith("./"):
            failures.append(f"Invalid asset path: {key}")
            continue
        path = ROOT / value
        if not path.resolve().is_relative_to(ROOT.resolve()) or path.is_symlink() or not path.is_file():
            failures.append(f"Missing or unsafe asset: {value}")
            continue
        data = path.read_bytes()
        if len(data) > 5 * 1024 * 1024 or data[:8] != b"\x89PNG\r\n\x1a\n":
            failures.append(f"Expected a PNG no larger than 5 MiB: {value}")
            continue
        width, height = struct.unpack(">II", data[16:24])
        if width != height or not 48 <= width <= 4096:
            failures.append(f"Icon must be square, 48–4096 pixels: {value}")
    color = interface.get("brandColor")
    if color:
        if not re.fullmatch(r"#[0-9A-Fa-f]{6}", color):
            failures.append("Invalid brandColor")
        else:
            rgb = [int(color[i:i+2], 16) / 255 for i in (1, 3, 5)]
            linear = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in rgb]
            luminance = sum(c * w for c, w in zip(linear, (.2126, .7152, .0722)))
            if 1.05 / (luminance + .05) < 2:
                failures.append("brandColor needs at least 2:1 contrast with white")
    for path in (ROOT / "skills").rglob("*"):
        if path.is_symlink():
            failures.append(f"Symlink in skills: {path.relative_to(ROOT)}")
    if not (ROOT / "skills/dialectical/SKILL.md").is_file():
        failures.append("Missing entry skill")
    return failures


def main() -> int:
    failures = validate()
    if failures:
        print("\n".join(failures))
        return 1
    print("Skills-only plugin package validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
