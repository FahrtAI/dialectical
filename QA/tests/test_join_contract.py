"""Static contract checks for the JOIN conversational handle."""
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class JoinContractTests(unittest.TestCase):
    def setUp(self):
        self.reference = (ROOT / "skills/dialectical/references/join.md").read_text()

    def test_join_is_a_core_handle_not_a_standalone_skill(self):
        self.assertFalse((ROOT / "skills/dialectical-join").exists())
        self.assertIn("conversational handle", self.reference)

    def test_menu_contract_has_four_ordered_choices(self):
        menu = [line for line in self.reference.splitlines()
                if line.startswith(("[1]", "[2]", "[3]", "[4]"))]
        self.assertEqual(menu, [
            "[1] RECAP — Recap what we have discussed.",
            "[2] DISTILL — Extract findings and remaining uncertainties.",
            "[3] TRACE — Reconstruct how the thinking developed.",
            "[4] CONTINUE — Continue without retrospective processing.",
        ])


if __name__ == "__main__":
    unittest.main()
