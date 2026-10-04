#!/usr/bin/env python3
"""Validate Dialectical's skill layout and local Markdown references."""

from __future__ import annotations

import re
import sys
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
# Working notes may name obsolete paths while describing a migration.
UNSCANNED = {"PUNCHLIST.md"}


def field(frontmatter: str, name: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(name)}:\s*(.+?)\s*$", frontmatter)
    return match.group(1).strip().strip('"\'') if match else None


def section(text: str, heading: str) -> str:
    match = re.search(rf"(?ms)^## {re.escape(heading)}\n(.*?)(?=^## |\Z)", text)
    return match.group(1) if match else ""


def main() -> int:
    failures: list[str] = []
    skill_files = sorted(SKILLS.glob("*/SKILL.md"))

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

        name = field(match.group("body"), "name")
        description = field(match.group("body"), "description")
        if name != path.parent.name:
            failures.append(
                f"Skill name {name!r} does not match directory {path.parent.name!r}"
            )
        if not description:
            failures.append(f"Missing description: {path.relative_to(ROOT)}")

        for target in LINK.findall(text):
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                failures.append(
                    f"Broken local link in {path.relative_to(ROOT)}: {target}"
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
        if ".dialectical" not in path.parts and path.name not in UNSCANNED
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
