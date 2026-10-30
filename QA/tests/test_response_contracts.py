"""Static checks for the shared response and calibration contract."""
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
COMMANDS = {
    "dialectical-ach": "ACH",
    "dialectical-causal-chain": "CAUSAL-CHAIN",
    "dialectical-challenge": "CHALLENGE",
    "dialectical-checkpoint": "CHECKPOINT",
    "dialectical-close": "CLOSE",
    "dialectical-collection-gaps": "COLLECTION GAPS",
    "dialectical-distill": "DISTILL",
    "dialectical-guide": "GUIDE",
    "dialectical-hypothesize": "HYPOTHESIZE",
    "dialectical-indicators": "INDICATORS",
    "dialectical-recall": "RECALL",
    "dialectical-recap": "RECAP",
    "dialectical-relevance": "RELEVANCE",
    "dialectical-research": "RESEARCH",
    "dialectical-restate": "RESTATE",
    "dialectical-resume": "RESUME",
    "dialectical-save": "SAVE",
    "dialectical-source-quality": "SOURCE-QUALITY",
    "dialectical-start-inquiry": "START INQUIRY",
    "dialectical-tag": "TAG",
    "dialectical-test-design": "TEST DESIGN",
    "dialectical-thought-experiment": "THOUGHT EXPERIMENT",
    "dialectical-trace": "TRACE",
    "dialectical-verify": "VERIFY",
}


class ResponseContractTests(unittest.TestCase):
    def test_every_operation_has_concision_calibration_and_learning_cue(self):
        for directory, command in COMMANDS.items():
            text = (ROOT / "skills" / directory / "SKILL.md").read_text()
            with self.subTest(skill=directory):
                self.assertIn("shortest complete", text.lower())
                self.assertIn(f"`{command} —", text)
                self.assertRegex(text.lower(), r"(evidence|claim|premise|uncertainty)")

    def test_core_defines_when_cues_apply(self):
        text = (ROOT / "skills/dialectical/SKILL.md").read_text()
        self.assertIn("## Response discipline", text)
        self.assertIn("ordinary-language request", text)
        self.assertIn("internal technique", text)
        self.assertIn("shortest complete response", text)

    def test_hold_or_update_is_named_first_and_reinforced(self):
        core = (ROOT / "skills/dialectical/SKILL.md").read_text()
        self.assertIn("## Hold or update on reasons", core)
        self.assertLess(core.index("## Hold or update on reasons"),
                        core.index("## Response discipline"))
        for phrase in ("Pressure is not a reason", "A reason is a reason",
                       "Earlier agreement is not evidence"):
            self.assertIn(phrase, core)
        for directory in ("dialectical-challenge", "dialectical-verify", "dialectical-distill"):
            with self.subTest(skill=directory):
                text = (ROOT / "skills" / directory / "SKILL.md").read_text()
                self.assertIn("Hold or update on reasons", text)

    def test_known_calibration_findings_are_fixed(self):
        example = (ROOT / "skills/dialectical-ach/references/example.md").read_text()
        source = (ROOT / "skills/dialectical-source-quality/SKILL.md").read_text()
        challenge = (ROOT / "skills/dialectical-challenge/SKILL.md").read_text()
        self.assertIn("group sizes, conversion counts", example)
        self.assertIn("not an automatic credibility upgrade", source)
        self.assertIn("does not verify or validate", challenge)


if __name__ == "__main__":
    unittest.main()
