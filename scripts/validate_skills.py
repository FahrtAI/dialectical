#!/usr/bin/env python3
"""Validate Dialectical's skill layout and local Markdown references."""

from __future__ import annotations

import re
import json
import sys
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
ROUTER = SKILLS / "dialectical" / "SKILL.md"
CASES = ROOT / "evals" / "cases.yaml"
FRONTMATTER = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.DOTALL)
LINK = re.compile(r"\[[^\]]+\]\((?!https?://|#)([^)]+)\)")
OBSOLETE = (
    "skills/primatives",
    "../primatives/",
    "NEW CONVO",
    "dialectical-alternative-hypotheses",
    "dialectical-source-quality-admiralty",
    "references/ach.md",
)
# Top-level keys accepted by both the Claude Code and Codex skill validators.
ALLOWED_KEYS = {"name", "description", "license", "allowed-tools", "metadata"}
SEMVER = re.compile(r"\d+\.\d+\.\d+")


def field(frontmatter: str, name: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(name)}:\s*(.+?)\s*$", frontmatter)
    return match.group(1).strip().strip('"\'') if match else None


def metadata_field(frontmatter: str, name: str) -> str | None:
    block = re.search(r"(?m)^metadata:[ \t]*\n((?:[ \t]+\S.*(?:\n|\Z))*)", frontmatter)
    return field(textwrap.dedent(block.group(1)), name) if block else None


def section(text: str, heading: str) -> str:
    match = re.search(rf"(?ms)^## {re.escape(heading)}\n(.*?)(?=^## |\Z)", text)
    return match.group(1) if match else ""


def main() -> int:
    failures: list[str] = []
    skill_files = sorted(SKILLS.glob("*/SKILL.md"))
    release = json.loads((ROOT / "plugin.json").read_text())["version"]

    if not skill_files:
        failures.append("No direct child skills found under skills/")

    nested = [path for path in SKILLS.glob("*/*/SKILL.md")]
    if nested:
        failures.extend(f"Nested undiscoverable skill: {path.relative_to(ROOT)}" for path in nested)

    for path in skill_files:
        text = path.read_text(encoding="utf-8")
        match = FRONTMATTER.match(text)
        if not match:
            failures.append(f"Missing YAML frontmatter: {path.relative_to(ROOT)}")
            continue

        body = match.group("body")
        name = field(body, "name")
        description = field(body, "description")
        if name != path.parent.name:
            failures.append(
                f"Skill name {name!r} does not match directory {path.parent.name!r}"
            )
        if not description:
            failures.append(f"Missing description: {path.relative_to(ROOT)}")
        if not name or len(name) > 64 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            failures.append(f"Invalid skill name: {name!r}")
        if description and len(description) > 1024:
            failures.append(f"Description too long: {path.relative_to(ROOT)}")

        unexpected = sorted(set(re.findall(r"(?m)^([A-Za-z][\w-]*):", body)) - ALLOWED_KEYS)
        if unexpected:
            failures.append(
                f"Unexpected frontmatter key(s) in {path.relative_to(ROOT)}: {', '.join(unexpected)}"
            )
        version = metadata_field(body, "version")
        if version != release:
            failures.append(f"Skill release differs from plugin: {path.relative_to(ROOT)}")
        if not version or not SEMVER.fullmatch(version):
            failures.append(
                f"Missing or non-semver metadata.version in {path.relative_to(ROOT)}: {version!r}"
            )

    for path in SKILLS.rglob("*.md"):
        for target in LINK.findall(path.read_text(encoding="utf-8")):
            resolved = (path.parent / target.split("#", 1)[0]).resolve()
            if not resolved.is_relative_to(SKILLS.resolve()) or not resolved.is_file():
                failures.append(
                    f"Missing or escaping skill link in {path.relative_to(ROOT)}: {target}"
                )

    route = section(ROUTER.read_text(encoding="utf-8"), "Route an invocation") if ROUTER.exists() else ""
    if not route:
        failures.append(f"Missing Route section: {ROUTER.relative_to(ROOT)}")
    cases = CASES.read_text(encoding="utf-8") if CASES.exists() else ""
    for path in skill_files:
        name = path.parent.name
        if route and name != "dialectical" and f"`{name}`" not in route:
            failures.append(f"Skill missing from router Route section: {name}")
        if not re.search(rf"(?m)^\s*(?:skill:|-)\s*{re.escape(name)}\s*$", cases):
            failures.append(f"Skill has no eval case in evals/cases.yaml: {name}")

    repository_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in ROOT.rglob("*.md")
        if ".dialectical" not in path.parts
    )
    for obsolete in OBSOLETE:
        if obsolete in repository_text:
            failures.append(f"Obsolete architecture reference remains: {obsolete}")

    if failures:
        print("Validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"Validated {len(skill_files)} directly discoverable skills.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
