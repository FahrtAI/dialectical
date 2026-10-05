#!/usr/bin/env python3
"""Validate Dialectical's portable and compatibility plugin manifests."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
SUBMISSION_CATEGORIES = {
    "Productivity",
    "Creativity",
    "Developer Tools",
    "Business & Operations",
    "Data & Analytics",
    "Communication",
    "Education & Research",
    "Security",
    "Finance",
    "Healthcare",
    "Travel",
    "Entertainment",
    "Other",
}


def load(path: Path, failures: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        failures.append(f"Cannot load {path.relative_to(ROOT)}: {error}")
        return {}
    if not isinstance(value, dict):
        failures.append(f"{path.relative_to(ROOT)} must contain an object")
        return {}
    return value


def validate(production: bool = False) -> list[str]:
    failures: list[str] = []
    portable = load(ROOT / "plugin.json", failures)
    mcp = load(ROOT / "mcp.json", failures)
    compatibility = load(ROOT / ".codex-plugin" / "plugin.json", failures)
    compatibility_mcp = load(ROOT / ".mcp.json", failures)

    for field in ("name", "version", "description"):
        if not isinstance(portable.get(field), str) or not portable[field].strip():
            failures.append(f"plugin.json requires non-empty {field}")
    if portable.get("name") != "dialectical":
        failures.append("plugin.json name must be dialectical")
    if not SEMVER.fullmatch(str(portable.get("version", ""))):
        failures.append("plugin.json version must be strict semver")
    for field in ("name", "version", "description"):
        if compatibility.get(field) != portable.get(field):
            failures.append(f"Compatibility manifest {field} must match plugin.json")

    servers = mcp.get("mcpServers")
    if not isinstance(servers, dict) or not servers:
        failures.append("mcp.json requires at least one MCP server")
    else:
        for name, config in servers.items():
            if not isinstance(config, dict):
                failures.append(f"MCP server {name} must be an object")
                continue
            if config.get("type") != "streamable-http":
                failures.append(f"Portable MCP server {name} must use streamable-http")
            url = config.get("url")
            parsed = urlparse(url) if isinstance(url, str) else None
            if parsed is None or not parsed.scheme or not parsed.netloc:
                failures.append(f"MCP server {name} requires an absolute URL")
            elif production and parsed.scheme != "https":
                failures.append(f"Production MCP server {name} must use HTTPS")
            elif production and parsed.hostname in {"localhost", "127.0.0.1", "::1"}:
                failures.append(f"Production MCP server {name} cannot use localhost")

    compat_servers = compatibility_mcp.get("mcpServers")
    if not isinstance(compat_servers, dict) or set(compat_servers) != set(servers or {}):
        failures.append("Portable and compatibility MCP server names must match")

    skill_files = sorted((ROOT / "skills").glob("*/SKILL.md"))
    if len(skill_files) != 20:
        failures.append(f"Expected 20 bundled skills, found {len(skill_files)}")

    interface = (
        portable.get("extensions", {}).get("com.openai", {}).get("interface", {})
        if isinstance(portable.get("extensions"), dict)
        else {}
    )
    compatibility_interface = compatibility.get("interface", {})
    if compatibility_interface != interface:
        failures.append("Portable and compatibility interface metadata must match")
    text_limits = {
        "displayName": 30,
        "shortDescription": 30,
        "longDescription": 4000,
        "developerName": 80,
    }
    for field, limit in text_limits.items():
        value = interface.get(field)
        if not isinstance(value, str) or not value.strip():
            failures.append(f"Plugin requires non-empty interface.{field}")
        elif len(value) > limit:
            failures.append(f"interface.{field} exceeds the {limit}-character submission limit")
    if interface.get("category") not in SUBMISSION_CATEGORIES:
        failures.append("interface.category is not a supported submission category")
    capabilities = interface.get("capabilities")
    if not isinstance(capabilities, list) or not capabilities or len(capabilities) > 20:
        failures.append("interface.capabilities must contain 1 to 20 entries")
    elif any(not isinstance(item, str) or not item.strip() or len(item) > 120 for item in capabilities):
        failures.append("Each interface capability must be non-empty and at most 120 characters")
    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list) or not prompts or len(prompts) > 3:
        failures.append("interface.defaultPrompt must contain 1 to 3 entries")
    elif any(not isinstance(item, str) or not item.strip() or len(item) > 128 for item in prompts):
        failures.append("Each starter prompt must be non-empty and at most 128 characters")
    if production:
        for field in ("websiteURL", "privacyPolicyURL", "termsOfServiceURL", "supportURL"):
            value = interface.get(field)
            parsed = urlparse(value) if isinstance(value, str) else None
            if parsed is None or parsed.scheme != "https" or not parsed.netloc:
                failures.append(f"Production plugin requires interface.{field}")

    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--production", action="store_true")
    args = parser.parse_args()
    failures = validate(production=args.production)
    if failures:
        print("Plugin package validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    mode = "production" if args.production else "development"
    print(f"Plugin package validation passed ({mode}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
