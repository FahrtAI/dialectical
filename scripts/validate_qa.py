#!/usr/bin/env python3
"""Audit all case definitions; defer unavailable fixtures without inventing passes."""
import argparse
import json
from run_evals import ROOT, cases_from, prerequisites


def audit():
    seen = set()
    results = []
    files = sorted((ROOT / "QA/cases").glob("*.yaml")) + [ROOT / "evals/cases.yaml"]
    for path in files:
        for case in cases_from(path):
            if case["id"] in seen:
                raise ValueError(f"Duplicate global case ID: {case['id']}")
            seen.add(case["id"])
            reasons = prerequisites(case)
            if path.name == "smoke.yaml" and reasons:
                raise ValueError(f"Smoke case has missing prerequisites: {case['id']}: {reasons}")
            results.append({"suite": str(path.relative_to(ROOT)), "id": case["id"],
                            "status": "deferred" if reasons else "inputs-ready",
                            "reasons": reasons})
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    results = audit()
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        deferred = sum(r["status"] == "deferred" for r in results)
        print(f"Validated {len(results)} case definitions; {deferred} deferred. No behavior executed.")
