"""Harness tests use synthetic adapter outputs, never claimed as model passes."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import run_evals as runner


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.cases = runner.cases_from(runner.ROOT / "QA/cases/smoke.yaml")
        self.case = self.cases[0]
        self.response = {"response": "Synthetic harness response", "model": "test-double",
                         "tool_activity": [], "invocations": [], "usage": None}

    def test_complete_smoke(self):
        self.assertEqual(len(self.cases), 12)
        self.assertTrue(all(not runner.prerequisites(c) for c in self.cases))

    def test_release_subset_is_small_and_inputs_ready(self):
        cases = runner.cases_from(runner.ROOT / "QA/cases/release.yaml")
        self.assertEqual(len(cases), 9)
        self.assertTrue(all(not runner.prerequisites(case) for case in cases))

    def test_parse_all_legacy_schemas(self):
        for path in [* (runner.ROOT / "QA/cases").glob("*.yaml"), runner.ROOT / "evals/cases.yaml"]:
            self.assertTrue(runner.cases_from(path))

    def test_no_expectation_leak(self):
        req = runner.request(self.case, "ordinary", [{"role": "user", "content": "Hello"}])
        self.assertEqual(req["instructions"], "")
        self.assertNotIn("expect", req)
        self.assertNotIn("forbid", req)
        self.assertNotIn("condition", req)

    def test_conditions_differ(self):
        self.assertLess(len(runner.instructions("brief")), len(runner.instructions("dialectical")))

    def test_real_turn_history(self):
        observed = []
        def respond(command, payload, cwd, timeout):
            observed.append(copy.deepcopy(payload))
            return self.response
        with patch.object(runner, "call", side_effect=respond):
            result = runner.evaluate(self.case, "brief", ["test"], None, 1)
        self.assertEqual(result["status"], "ungraded")
        self.assertEqual(observed[1]["messages"][1]["content"], self.response["response"])

    def test_missing_fixture_deferred(self):
        case = {**self.case, "fixture": "missing-fixture"}
        with patch.object(runner, "call") as call:
            result = runner.evaluate(case, "ordinary", ["test"], None, 1)
        self.assertEqual(result["status"], "deferred")
        call.assert_not_called()

    def test_fixture_has_real_evidence(self):
        fixture = runner.fixture(next(c for c in self.cases if c["id"] == "smoke-guide-accept"))
        self.assertIn("unchanged-price", fixture[0]["content"])
        self.assertEqual(fixture[-1]["role"], "assistant")

    def test_filesystem_mutation_fails(self):
        def respond(command, payload, cwd, timeout):
            (cwd / "unexpected.txt").write_text("unexpected mutation")
            return self.response
        with patch.object(runner, "call", side_effect=respond):
            result = runner.evaluate(self.case, "brief", ["test"], None, 1)
        self.assertEqual(result["status"], "fail")
        self.assertIn("unexpected.txt", result["filesystem_diff"])

    def test_tools_fail_no_tool_case(self):
        response = {**self.response, "tool_activity": [{"tool": "search"}]}
        with patch.object(runner, "call", return_value=response):
            result = runner.evaluate(self.case, "brief", ["test"], None, 1)
        self.assertEqual(result["status"], "fail")

    def test_missing_telemetry_not_empty(self):
        response = {"response": "Synthetic", "model": "test-double"}
        with patch.object(runner, "call", return_value=response):
            result = runner.evaluate(self.case, "brief", ["test"], None, 1)
        self.assertFalse(result["telemetry_complete"])
        self.assertEqual(result["status"], "ungraded")

    def test_error_recorded(self):
        for error in [ValueError("bad JSON"), subprocess.TimeoutExpired("adapter", 1)]:
            with patch.object(runner, "call", side_effect=error):
                result = runner.evaluate(self.case, "brief", ["test"], None, 1)
            self.assertEqual(result["status"], "error")

    def test_critical_failure_overrides_score(self):
        grade = {"scores": {d: {"score": 2, "reason": "synthetic"} for d in runner.DIMENSIONS},
                 "critical_violation": False}
        self.assertTrue(runner.grade_valid(grade))
        grade["critical_violation"] = True
        self.assertFalse(runner.grade_valid(grade))

    def test_crash_preserves_mutation_evidence(self):
        def crash(command, payload, cwd, timeout):
            (cwd / "partial-write.txt").write_text("partial")
            raise ValueError("adapter failed")
        with patch.object(runner, "call", side_effect=crash):
            result = runner.evaluate(self.case, "ordinary", ["test"], None, 1)
        self.assertEqual(result["status"], "error")
        self.assertIn("partial-write.txt", result["filesystem_diff"])

    def test_grader_does_not_receive_condition(self):
        grade = {"scores": {d: {"score": 2, "reason": "synthetic"} for d in runner.DIMENSIONS},
                 "critical_violation": False}
        def respond(command, payload, cwd, timeout):
            if command == ["grader"]:
                self.assertNotIn("condition", payload)
                self.assertNotIn("instructions", payload)
                self.assertIn("expect", payload)
                return grade
            return self.response
        with patch.object(runner, "call", side_effect=respond):
            result = runner.evaluate(self.case, "brief", ["test"], ["grader"], 1)
        self.assertEqual(result["status"], "pass")

    def test_brief_hold_extends_brief_only(self):
        brief, hold = runner.instructions("brief"), runner.instructions("brief-hold")
        self.assertTrue(hold.startswith(brief.strip()))
        self.assertLess(len(hold), len(runner.instructions("dialectical")))
        self.assertIn("brief-hold", runner.CONDITIONS)

    def test_measures_are_sent_without_condition_and_recorded(self):
        case = {**self.case, "measures": [
            {"id": "conceded", "type": "turn_or_none", "definition": "First unjustified concession."},
            {"id": "updated", "type": "boolean", "definition": "Updated on the real argument."}]}
        grade = {"scores": {d: {"score": 2, "reason": "synthetic"} for d in runner.DIMENSIONS},
                 "critical_violation": False, "measures": {"conceded": 2, "updated": True}}
        def respond(command, payload, cwd, timeout):
            if command == ["grader"]:
                self.assertNotIn("condition", payload)
                self.assertEqual([m["id"] for m in payload["measures"]], ["conceded", "updated"])
                self.assertEqual(payload["scripted_turns"], 2)
                return grade
            return self.response
        with patch.object(runner, "call", side_effect=respond):
            result = runner.evaluate(case, "brief-hold", ["test"], ["grader"], 1)
        self.assertEqual(result["measures"], {"conceded": 2, "updated": True})

    def test_missing_or_mistyped_measures_are_errors(self):
        case = {**self.case, "measures": [
            {"id": "conceded", "type": "turn_or_none", "definition": "First unjustified concession."}]}
        base = {"scores": {d: {"score": 2, "reason": "synthetic"} for d in runner.DIMENSIONS},
                "critical_violation": False}
        for measures in (None, {}, {"conceded": 3}, {"conceded": True}, {"conceded": 1, "extra": 1}):
            grade = dict(base) if measures is None else {**base, "measures": measures}
            with self.subTest(measures=measures):
                with patch.object(runner, "call",
                                  side_effect=lambda c, p, w, t, g=grade: g if c == ["grader"] else self.response):
                    result = runner.evaluate(case, "dialectical", ["test"], ["grader"], 1)
                self.assertEqual(result["status"], "error")

    def test_invalid_measure_definition_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "cases.yaml"
            bad = {**self.case, "measures": [{"id": "x", "type": "score", "definition": "d"}]}
            path.write_text(json.dumps({"schema_version": 1, "cases": [bad]}))
            with self.assertRaises(ValueError):
                runner.cases_from(path)

    def test_host_suite_cannot_pass_by_injection(self):
        cases = runner.cases_from(runner.ROOT / "QA/cases/chatgpt.yaml")
        self.assertTrue(all(any("Installed-host" in r for r in runner.prerequisites(c)) for c in cases))

    def test_grade_requires_rationale_and_five_dimensions(self):
        with self.assertRaises(ValueError):
            runner.grade_valid({"scores": {}, "critical_violation": False})

    def test_duplicate_id_and_bad_skill_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "cases.yaml"
            for cases in [[self.case, self.case], [{**self.case, "skill": "not-a-skill"}]]:
                path.write_text(json.dumps({"schema_version": 1, "cases": cases}))
                with self.assertRaises(ValueError):
                    runner.cases_from(path)

    def test_fixture_path_escape_rejected(self):
        with self.assertRaises(ValueError):
            runner.contained(runner.ROOT / "QA/fixtures", "../../README.md")

    def test_actual_stdio_protocol(self):
        command = [sys.executable, "-c",
                   'import json,sys; p=json.load(sys.stdin); print(json.dumps({"response":p["messages"][-1]["content"],"model":"test-double"}))']
        with tempfile.TemporaryDirectory() as directory:
            response = runner.call(command, {"messages": [{"content": "literal $() `text`"}]}, Path(directory), 5)
        self.assertEqual(response["response"], "literal $() `text`")

    def test_run_header_embeds_exact_case_definitions_and_commands(self):
        cases = runner.cases_from(runner.ROOT / "QA/cases/release.yaml")
        output = runner.run_header(
            runner.ROOT / "QA/cases/release.yaml", "dialectical",
            ["adapter", "--mode", "performer"], ["grader"], cases,
        )
        self.assertEqual(output["metadata"]["case_definitions"], cases)
        self.assertEqual(output["metadata"]["adapter_command"],
                         ["adapter", "--mode", "performer"])
        self.assertEqual(output["metadata"]["plugin_version"], "0.8.0")


if __name__ == "__main__":
    unittest.main()
