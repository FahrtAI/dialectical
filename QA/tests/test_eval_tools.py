"""Tests for optional evaluation adapters and recorded-run comparison."""
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts/adapters"))

import compare_runs
import openai_responses


class EvaluationToolTests(unittest.TestCase):
    def test_response_text_and_tool_activity(self):
        response = {
            "output": [
                {"type": "reasoning"},
                {"type": "message", "content": [
                    {"type": "output_text", "text": "Useful response"}
                ]},
                {"type": "function_call", "name": "unexpected"},
            ]
        }
        self.assertEqual(openai_responses.output_text(response), "Useful response")
        self.assertEqual(openai_responses.tool_activity(response), [
            {"type": "function_call", "name": "unexpected"}
        ])

    def test_adapter_request_disables_storage_and_configures_no_tools(self):
        body = openai_responses.request_body(
            {"instructions": "Be useful", "messages": [{"role": "user", "content": "Hi"}]},
            "explicit-model",
        )
        self.assertEqual(body["model"], "explicit-model")
        self.assertFalse(body["store"])
        self.assertNotIn("tools", body)

    def test_grade_parser_accepts_json_fence_only(self):
        grade = {"scores": {}, "critical_violation": False}
        self.assertEqual(openai_responses.parse_grade(
            "```json\n" + json.dumps(grade) + "\n```"), grade)

    def test_compare_marks_missing_metrics_unavailable(self):
        base = {"results": [{"case_id": "one", "status": "pass", "turns": [
            {"word_count": 10, "duration_seconds": 1.0, "usage": None}
        ]}]}
        candidate = {"results": [{"case_id": "one", "status": "pass", "turns": [
            {"word_count": 8, "duration_seconds": 2.0,
             "usage": {"total_tokens": 50}}
        ]}]}
        with tempfile.TemporaryDirectory() as directory:
            left = Path(directory) / "left.json"
            right = Path(directory) / "right.json"
            left.write_text(json.dumps(base))
            right.write_text(json.dumps(candidate))
            report = compare_runs.render(compare_runs.load(left), compare_runs.load(right), left, right)
        self.assertIn("10.0 → 8.0", report)
        self.assertIn("unavailable → 50.0", report)
        self.assertIn("shorter or cheaper is not automatically better", report)


    def test_measure_summary_counts_only(self):
        self.assertEqual(compare_runs.measure_summary([True, False, True]), "true 2/3")
        self.assertEqual(compare_runs.measure_summary([None, 4, None]), "none 2/3; turns [4]")
        self.assertEqual(compare_runs.measure_summary([]), "unavailable")

    def test_grader_prompt_includes_measures_only_when_declared(self):
        payload = {"rubric": "r", "expect": ["e"], "messages": []}
        self.assertNotIn("MEASURES", openai_responses.grade_body(payload, "m")["instructions"])
        payload.update(measures=[{"id": "conceded", "type": "turn_or_none", "definition": "d"}],
                       scripted_turns=3)
        text = openai_responses.grade_body(payload, "m")["instructions"]
        self.assertIn("MEASURES", text)
        self.assertIn("last 3 user messages", text)

if __name__ == "__main__":
    unittest.main()
