#!/usr/bin/env python3
"""Compare two recorded Dialectical evaluation runs without inventing metrics."""
from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path


def load(path: Path) -> dict:
    data = json.loads(path.read_text())
    if not isinstance(data, dict) or not isinstance(data.get("results"), list):
        raise ValueError(f"Invalid run artifact: {path}")
    return data


def number(values: list[float]) -> str:
    return "unavailable" if not values else f"{statistics.mean(values):.1f}"


def usage_total(turn: dict) -> float | None:
    usage = turn.get("usage")
    if not isinstance(usage, dict):
        return None
    for key in ("total_tokens", "total_token_count"):
        if isinstance(usage.get(key), (int, float)):
            return float(usage[key])
    return None


def summarize(data: dict) -> dict[str, dict]:
    grouped: dict[str, dict] = {}
    for result in data["results"]:
        case = result.get("case_id", "unknown")
        item = grouped.setdefault(case, {"statuses": [], "words": [], "duration": [],
                                         "tokens": [], "scores": [], "routing": [],
                                         "measures": {}})
        for name, value in (result.get("measures") or {}).items():
            item["measures"].setdefault(name, []).append(value)
        item["statuses"].append(result.get("status", "missing"))
        activation = result.get("activation", {})
        item["routing"].append(activation.get("pass") if activation else None)
        for turn in result.get("turns", []):
            if isinstance(turn.get("word_count"), (int, float)):
                item["words"].append(float(turn["word_count"]))
            if isinstance(turn.get("duration_seconds"), (int, float)):
                item["duration"].append(float(turn["duration_seconds"]))
            tokens = usage_total(turn)
            if tokens is not None:
                item["tokens"].append(tokens)
        grade = result.get("grade", {}).get("scores", {})
        if grade and all(isinstance(v.get("score"), int) for v in grade.values()):
            item["scores"].append(sum(v["score"] for v in grade.values()))
    return grouped


def status(values: list[str]) -> str:
    counts = {value: values.count(value) for value in sorted(set(values))}
    return ", ".join(f"{key}:{value}" for key, value in counts.items())


def routing(values: list[bool | None]) -> str:
    if not values or all(value is None for value in values):
        return "unavailable"
    return ",".join("pass" if value is True else "fail" if value is False else "n/a"
                    for value in values)


def measure_summary(values: list) -> str:
    """Counts only: booleans as true/n; turn measures as none/n plus observed turns."""
    if not values:
        return "unavailable"
    if all(isinstance(v, bool) for v in values):
        return f"true {sum(values)}/{len(values)}"
    turns = sorted(v for v in values if v is not None)
    held = len(values) - len(turns)
    return f"none {held}/{len(values)}" + (f"; turns {turns}" if turns else "")


def render(baseline: dict, candidate: dict, baseline_path: Path, candidate_path: Path) -> str:
    left, right = summarize(baseline), summarize(candidate)
    cases = sorted(set(left) | set(right))
    rows = [
        "# Dialectical run comparison",
        "",
        f"Baseline: `{baseline_path}`",
        f"Candidate: `{candidate_path}`",
        "",
        "| Case | Status B → C | Routing B → C | Mean words B → C | Mean tokens B → C | Mean seconds B → C | Mean score B → C |",
        "|---|---|---|---:|---:|---:|---:|",
    ]
    empty = {"statuses": ["missing"], "routing": [], "words": [], "tokens": [],
             "duration": [], "scores": []}
    for case in cases:
        a, b = left.get(case, empty), right.get(case, empty)
        rows.append(
            f"| {case} | {status(a['statuses'])} → {status(b['statuses'])} | "
            f"{routing(a['routing'])} → {routing(b['routing'])} | "
            f"{number(a['words'])} → {number(b['words'])} | "
            f"{number(a['tokens'])} → {number(b['tokens'])} | "
            f"{number(a['duration'])} → {number(b['duration'])} | "
            f"{number(a['scores'])} → {number(b['scores'])} |"
        )
    measured = sorted({(case, name) for side in (left, right)
                       for case, item in side.items() for name in item["measures"]})
    if measured:
        rows += ["", "## Primary measures", "",
                 "| Case | Measure | Baseline | Candidate |", "|---|---|---|---|"]
        for case, name in measured:
            a = left.get(case, empty).get("measures", {}).get(name, [])
            b = right.get(case, empty).get("measures", {}).get(name, [])
            rows.append(f"| {case} | {name} | {measure_summary(a)} | {measure_summary(b)} |")
    rows += ["", "`unavailable` means the adapter did not report that metric. Review the retained transcripts and grader rationales before drawing a conclusion; shorter or cheaper is not automatically better.", ""]
    return "\n".join(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = render(load(args.baseline), load(args.candidate), args.baseline, args.candidate)
    if args.output:
        if args.output.exists():
            parser.error("output already exists; choose a new path")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report)
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
