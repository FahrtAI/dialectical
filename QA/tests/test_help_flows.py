"""Static contracts for packaged help, cookbook, and flow references."""
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_plugin_package import package_files


RECIPES = (
    "Explore a new idea",
    "Explain an unexpected outcome",
    "Test a causal claim",
    "Make a decision under uncertainty",
    "Evaluate a source or claim",
    "Develop a strategy",
    "Compare competing explanations",
    "Work through disagreement",
    "Preserve a long inquiry",
)

PATHWAYS = ("Explore", "Explain", "Decide", "Evaluate", "Preserve", "Random question")


class HelpFlowContracts(unittest.TestCase):
    def setUp(self):
        references = ROOT / "skills/dialectical/references"
        self.help = (references / "help.md").read_text()
        self.cookbook = (references / "cookbook.md").read_text()
        self.flows = (references / "flows.md").read_text()

    def test_distinct_packaged_references_are_linked_and_included(self):
        packaged = {path.relative_to(ROOT).as_posix() for path in package_files()}
        for name in ("cookbook.md", "flows.md"):
            self.assertIn(f"]({name})", self.help)
            self.assertIn(f"skills/dialectical/references/{name}", packaged)

    def test_cookbook_contains_every_repository_recipe(self):
        repository = (ROOT / "docs/cookbook.md").read_text()
        for recipe in RECIPES:
            heading = f"## {recipe}"
            self.assertIn(heading, self.cookbook)
            self.assertIn(heading, repository)

    def test_flows_contain_every_generic_pathway(self):
        repository = (ROOT / "docs/flows.md").read_text()
        for pathway in PATHWAYS:
            self.assertIn(f"**{pathway}**", self.flows)
            self.assertIn(f"**{pathway}**", repository)

    def test_only_repository_flow_docs_use_mermaid(self):
        self.assertNotIn("```mermaid", self.cookbook)
        self.assertNotIn("```mermaid", self.flows)
        self.assertIn("```mermaid", (ROOT / "docs/flows.md").read_text())

    def test_orientation_does_not_authorize_operations(self):
        for text in (self.help, self.cookbook, self.flows):
            self.assertRegex(text, r"(?i)(does not|do not).* (invoke|run|start|apply)")


if __name__ == "__main__":
    unittest.main()
