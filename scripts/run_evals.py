#!/usr/bin/env python3
"""Maintainer-only recorded/adapter evaluations; never a plugin runtime.

Adapter: JSON request on stdin, JSON response on stdout. No shell execution.
See QA/RUNNING.md. Requires PyYAML only for reading the existing YAML corpus.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DIMENSIONS = ("routing", "operation", "calibration", "boundary", "usefulness")
INLINE = {None, "none", "conversation-in-prompt", "evidence-in-prompt",
          "claim-in-prompt", "plan-in-prompt"}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def contained(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError(f"Missing or escaping file: {relative}")
    return path


def fixture(case: dict) -> list[dict]:
    name = case.get("fixture", case.get("environment", {}).get("fixture"))
    if name in INLINE:
        return []
    registry = json.loads((ROOT / "QA/fixtures/registry.json").read_text())
    if name not in registry:
        raise ValueError(f"Undefined fixture: {name}")
    data = json.loads(contained(ROOT / "QA/fixtures", registry[name]).read_text())
    return data["messages"]


def messages_valid(messages: list) -> bool:
    return isinstance(messages, list) and all(
        isinstance(m, dict) and m.get("role") in {"user", "assistant"}
        and isinstance(m.get("content"), str) and bool(m["content"].strip())
        for m in messages)


def cases_from(path: Path) -> list[dict]:
    data = yaml.safe_load(path.read_text())
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError(f"Unsupported case schema: {path}")
    cases = data.get("cases")
    if not isinstance(cases, list):
        raise ValueError(f"Missing cases: {path}")
    names = set()
    skills = {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")}
    for case in cases:
        if not isinstance(case, dict) or not isinstance(case.get("id"), str):
            raise ValueError(f"Invalid case: {path}")
        if case["id"] in names:
            raise ValueError(f"Duplicate ID: {case['id']}")
        names.add(case["id"])
        case["environment"] = {**data.get("environment", {}), **case.get("environment", {})}
        referenced = case.get("skill", case.get("skills", []))
        referenced = [referenced] if isinstance(referenced, str) else list(referenced)
        activation = case.get("expect_activation", {})
        referenced += activation.get("include", []) + activation.get("exclude", [])
        if not referenced or any(s not in skills for s in referenced):
            raise ValueError(f"Invalid skill reference: {case['id']}")
        turns = case.get("turns", [case.get("prompt")])
        if not turns or any(not isinstance(t, str) or not t.strip() for t in turns):
            raise ValueError(f"Missing prompt/turns: {case['id']}")
        if not messages_valid(case.get("messages", [])):
            raise ValueError(f"Invalid messages: {case['id']}")
        if not isinstance(case.get("expect"), list) or not case["expect"]:
            raise ValueError(f"Missing expectations: {case['id']}")
    return cases


def prerequisites(case: dict) -> list[str]:
    reasons = []
    try:
        if not messages_valid(fixture(case)):
            reasons.append("Invalid fixture messages")
    except (ValueError, KeyError, OSError) as exc:
        reasons.append(str(exc))
    env = case.get("environment", {})
    if env.get("invocation") or env.get("plugin"):
        reasons.append("Installed-host adapter required; local injection is not host acceptance")
    if env.get("external_evidence") in {"available", "controlled", "live"}:
        reasons.append("Evidence-provider capability not configured")
    if env.get("isolated_workers") == "available" or case.get("expect_delegation"):
        reasons.append("Delegation trace capability not configured")
    if case.get("expected_mutation", {}).get("class", "none") != "none":
        reasons.append("File-mutation suite not enabled by this adapter protocol")
    return reasons


def instructions(condition: str) -> str:
    if condition == "ordinary":
        return ""
    if condition == "brief":
        return (ROOT / "QA/conditions/brief.txt").read_text()
    # Deliberate full entrypoint injection, not a claim of installed-host routing.
    paths = sorted((ROOT / "skills").glob("*/SKILL.md"))
    paths += [ROOT / "skills/dialectical/references/help.md",
              ROOT / "skills/dialectical/references/cookbook.md",
              ROOT / "skills/dialectical/references/flows.md",
              ROOT / "skills/dialectical/references/join.md",
              ROOT / "skills/dialectical/references/modes.md",
              ROOT / "skills/dialectical-save/references/handoff-format.md"]
    return "\n\n".join(f"{p.relative_to(ROOT)}\n{p.read_text()}" for p in paths)


def request(case: dict, condition: str, messages: list[dict]) -> dict:
    return {"protocol_version": 1, "instructions": instructions(condition),
            "messages": messages, "capabilities": {"external_evidence": False,
            "filesystem": False, "workers": False}}


def call(command: list[str], payload: dict, cwd: Path, timeout: float) -> dict:
    result = subprocess.run(command, input=json.dumps(payload), text=True,
                            capture_output=True, cwd=cwd, timeout=timeout)
    if result.returncode:
        # Do not echo arbitrary adapter stderr: it may contain credentials.
        raise ValueError(f"Adapter exited {result.returncode}; inspect it locally")
    try:
        data = json.loads(result.stdout)
    except ValueError as exc:
        raise ValueError("Adapter did not return JSON") from exc
    if not isinstance(data, dict):
        raise ValueError("Adapter response must be an object")
    return data


def snapshot(root: Path) -> dict:
    return {str(p.relative_to(root)): digest(p.read_bytes())
            for p in root.rglob("*") if p.is_file() and not p.is_symlink()}


def validate_response(data: dict) -> None:
    if not isinstance(data.get("response"), str) or not data["response"].strip():
        raise ValueError("Missing/nonempty response required")
    if not isinstance(data.get("model"), str) or not data["model"].strip():
        raise ValueError("Adapter must identify its model")
    for field in ("tool_activity", "invocations"):
        if data.get(field) is not None and not isinstance(data[field], list):
            raise ValueError(f"{field} must be a list or null")
    if data.get("invocations") is not None:
        invocation_names(data["invocations"])
    if data.get("usage") is not None and not isinstance(data["usage"], dict):
        raise ValueError("usage must be an object or null")


def invocation_names(items: list | None) -> set[str] | None:
    """Normalize skill-invocation telemetry without inferring it from prose."""
    if items is None:
        return None
    names = set()
    for item in items:
        if isinstance(item, str) and item.strip():
            names.add(item.strip())
        elif (isinstance(item, dict) and isinstance(item.get("skill"), str)
              and item["skill"].strip()):
            names.add(item["skill"].strip())
        else:
            raise ValueError(
                "Each invocation must be a skill-name string or object with a nonempty skill field"
            )
    return names


def activation_result(case: dict, turns: list[dict]) -> dict:
    expected = case.get("expect_activation")
    if expected is None:
        return {"required": False, "pass": True, "observed": []}
    observed = set()
    for turn in turns:
        names = invocation_names(turn.get("invocations"))
        if names is None:
            return {"required": True, "pass": None,
                    "reason": "Invocation telemetry unavailable"}
        observed.update(names)
    included = set(expected.get("include", []))
    excluded = set(expected.get("exclude", []))
    missing = sorted(included - observed)
    forbidden = sorted(excluded & observed)
    return {"required": True, "pass": not missing and not forbidden,
            "observed": sorted(observed), "missing": missing,
            "forbidden": forbidden}


def grade_valid(grade: dict) -> bool:
    scores = grade.get("scores", {})
    if set(scores) != set(DIMENSIONS):
        raise ValueError("Grader must score all five canonical dimensions")
    for value in scores.values():
        if (not isinstance(value, dict) or type(value.get("score")) is not int
                or value["score"] not in (0, 1, 2)
                or not isinstance(value.get("reason"), str) or not value["reason"].strip()):
            raise ValueError("Each grade needs a 0–2 integer score and rationale")
    if type(grade.get("critical_violation")) is not bool:
        raise ValueError("Grader must explicitly assess critical violations")
    return (sum(v["score"] for v in scores.values()) >= 9
            and scores["routing"]["score"] > 0 and scores["boundary"]["score"] > 0
            and not grade["critical_violation"])


def metadata(suite: Path) -> dict:
    def git(*args):
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()
    return {"created": datetime.now(timezone.utc).isoformat(),
            "commit": git("rev-parse", "HEAD"), "dirty_state": git("status", "--porcelain"),
            "plugin_version": json.loads((ROOT / "plugin.json").read_text())["version"],
            "suite": str(suite), "suite_hash": digest(suite.read_bytes()),
            "skill_hashes": {str(p.relative_to(ROOT)): digest(p.read_bytes())
                             for p in sorted((ROOT / "skills").rglob("*.md"))},
            "rubric_hash": digest((ROOT / "evals/SCORING.md").read_bytes()),
            "host": "adapter, not installed ChatGPT", "protocol_version": 1}


def run_header(suite: Path, condition: str, adapter: list[str],
               grader: list[str] | None, cases: list[dict]) -> dict:
    return {"metadata": {**metadata(suite),
                         "adapter_command": adapter,
                         "grader_command": grader,
                         "case_definitions": cases},
            "condition": condition,
            "instruction_hash": digest(instructions(condition).encode()),
            "results": []}


def evaluate(case: dict, condition: str, adapter: list[str], grader: list[str] | None,
             timeout: float) -> dict:
    record = {"case_id": case["id"], "condition": condition, "status": "ungraded",
              "retries": 0, "turns": []}
    reasons = prerequisites(case)
    if reasons:
        return {**record, "status": "deferred", "reasons": reasons}
    messages = fixture(case) + case.get("messages", [])
    record["initial_messages"] = list(messages)
    with tempfile.TemporaryDirectory(prefix="dialectical-eval-") as temporary:
        cwd = Path(temporary)
        before = snapshot(cwd)
        try:
            for user in case.get("turns", [case.get("prompt")]):
                messages.append({"role": "user", "content": user})
                started = time.monotonic()
                result = call(adapter, request(case, condition, messages), cwd, timeout)
                validate_response(result)
                record["turns"].append({"user": user, **result,
                    "duration_seconds": time.monotonic() - started,
                    "word_count": len(result["response"].split())})
                messages.append({"role": "assistant", "content": result["response"]})
            after = snapshot(cwd)
            diff = {p: {"before": before.get(p), "after": after.get(p)}
                    for p in before.keys() | after.keys() if before.get(p) != after.get(p)}
            observed_tools = [t for turn in record["turns"]
                              for t in (turn.get("tool_activity") or [])]
            record["filesystem_diff"] = diff
            record["deterministic_pass"] = not diff and not observed_tools
            record["telemetry_complete"] = all(
                turn.get("tool_activity") is not None and turn.get("invocations") is not None
                for turn in record["turns"])
            record["activation"] = activation_result(case, record["turns"])
            if grader:
                grading = {"protocol_version": 1, "rubric": (ROOT / "evals/SCORING.md").read_text(),
                           "expect": case["expect"], "forbid": case.get("forbid", []),
                           "expect_activation": case.get("expect_activation"),
                           "observed_invocations": record["activation"].get("observed"),
                           "messages": messages}
                # The grader receives neither condition nor performer self-assessment.
                record["grade"] = call(grader, grading, cwd, timeout)
                semantic_pass = grade_valid(record["grade"])
                activation_pass = record["activation"]["pass"]
                passed = semantic_pass and record["deterministic_pass"] and activation_pass is True
                if passed:
                    record["status"] = "pass"
                elif activation_pass is None and semantic_pass and record["deterministic_pass"]:
                    record["status"] = "ungraded"
                    record["reasons"] = ["Invocation telemetry required for routing assertion"]
                else:
                    record["status"] = "fail"
            elif not record["deterministic_pass"]:
                record["status"] = "fail"
            elif record["activation"]["pass"] is False:
                record["status"] = "fail"
        except (ValueError, OSError, subprocess.TimeoutExpired) as exc:
            record.update(status="error", error=str(exc))
        finally:
            # Preserve mutation evidence even when an adapter crashes or times out.
            after = snapshot(cwd)
            record["filesystem_diff"] = {
                p: {"before": before.get(p), "after": after.get(p)}
                for p in before.keys() | after.keys() if before.get(p) != after.get(p)}
            if record["filesystem_diff"]:
                record["deterministic_pass"] = False
                if record["status"] != "error":
                    record["status"] = "fail"
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["validate", "run"])
    parser.add_argument("--suite", type=Path, default=ROOT / "QA/cases/smoke.yaml")
    parser.add_argument("--condition", choices=["ordinary", "brief", "dialectical"], default="dialectical")
    parser.add_argument("--case", action="append", dest="selected")
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument("--adapter", nargs="+", help="Executable and arguments; absolute script paths recommended")
    parser.add_argument("--grader", nargs="+")
    parser.add_argument("--timeout", type=float, default=120)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.repeat < 1 or args.timeout <= 0:
        parser.error("repeat and timeout must be positive")
    cases = cases_from(args.suite)
    if args.selected:
        unknown = set(args.selected) - {c["id"] for c in cases}
        if unknown:
            parser.error(f"Unknown cases: {sorted(unknown)}")
        cases = [c for c in cases if c["id"] in args.selected]
    if args.action == "validate":
        report = [{"id": c["id"], "prerequisites": prerequisites(c)} for c in cases]
        print(json.dumps(report, indent=2))
        return 1 if any(r["prerequisites"] for r in report) else 0
    if not args.adapter or not args.output:
        parser.error("run requires --adapter and --output")
    if args.output.exists():
        parser.error("output already exists; choose a new artifact path")
    if args.grader == args.adapter:
        parser.error("use a separate grader command/session, not the performer")
    # Resolve executables before switching each run to its isolated fixture directory.
    for command in (args.adapter, args.grader):
        if command:
            command[0] = shutil.which(command[0]) or command[0]
    output = run_header(args.suite, args.condition, args.adapter, args.grader, cases)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    for repeat in range(args.repeat):
        for case in cases:
            record = evaluate(case, args.condition, args.adapter, args.grader, args.timeout)
            record["repeat"] = repeat + 1
            output["results"].append(record)
            args.output.write_text(json.dumps(output, indent=2) + "\n")
            print(case["id"], repeat + 1, record["status"], flush=True)
    # An ungraded/deferred run is intentionally not a passing process result.
    return 0 if all(r["status"] == "pass" for r in output["results"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
