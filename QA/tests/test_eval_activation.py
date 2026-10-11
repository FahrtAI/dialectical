"""Contract checks for structured skill-activation telemetry."""
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from run_evals import activation_result, invocation_names


class EvalActivationTests(unittest.TestCase):
    def test_invocation_names_accepts_documented_shapes(self):
        self.assertEqual(
            invocation_names(["dialectical-guide", {"skill": "dialectical-ach"}]),
            {"dialectical-guide", "dialectical-ach"},
        )

    def test_activation_checks_required_and_forbidden_skills(self):
        case = {"expect_activation": {
            "include": ["dialectical-ach"],
            "exclude": ["dialectical-guide"],
        }}
        result = activation_result(case, [{"invocations": ["dialectical-guide"]}])
        self.assertFalse(result["pass"])
        self.assertEqual(result["missing"], ["dialectical-ach"])
        self.assertEqual(result["forbidden"], ["dialectical-guide"])

    def test_missing_telemetry_cannot_pass_routing(self):
        case = {"expect_activation": {"include": ["dialectical-save"], "exclude": []}}
        result = activation_result(case, [{"invocations": None}])
        self.assertIsNone(result["pass"])


if __name__ == "__main__":
    unittest.main()
