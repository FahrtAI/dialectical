"""Release integrity tests; these do not execute ChatGPT behavior."""
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import warnings
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import package_plugin as package


class ArchiveTests(unittest.TestCase):
    def test_stable_bytes_despite_order_mtime_and_mode(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first, second = root / "first.md", root / "second.md"
            first.write_text("one")
            second.write_text("two")
            with patch.object(package, "ROOT", root):
                before = package.archive_bytes(package.package_inputs([first, second]))
                os.utime(first, (1234567890, 1234567890))
                first.chmod(0o755)
                after = package.archive_bytes(package.package_inputs([second, first]))
            self.assertEqual(before, after)

    def test_changed_content_changes_digest(self):
        first = package.archive_bytes({"a.md": b"one"})
        second = package.archive_bytes({"a.md": b"two"})
        self.assertNotEqual(hashlib.sha256(first).digest(), hashlib.sha256(second).digest())

    def test_reject_extra_missing_and_modified_contents(self):
        expected = {"a.md": b"one"}
        for inputs in [{}, {"a.md": b"two"}, {**expected, "server.py": b"extra"}]:
            with self.subTest(inputs=inputs), self.assertRaises(ValueError):
                package.verify_archive(package.archive_bytes(inputs), expected)

    def test_duplicate_member_rejected(self):
        data = io.BytesIO()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(data, "w") as archive:
                archive.writestr("a.md", b"one")
                archive.writestr("a.md", b"one")
        with self.assertRaises(ValueError):
            package.verify_archive(data.getvalue(), {"a.md": b"one"})

    def test_symlink_input_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "source").write_text("text")
            link = root / "link.md"
            link.symlink_to(root / "source")
            with patch.object(package, "ROOT", root), self.assertRaises(ValueError):
                package.package_inputs([link])

    def test_real_build_checksums_manifest_and_exclusions(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(package.main(["--output-dir", directory]), 0)
            archive = next(Path(directory).glob("*.zip"))
            record = json.loads(archive.with_suffix(".build.json").read_text())
            digest = hashlib.sha256(archive.read_bytes()).hexdigest()
            self.assertEqual(record["sha256"], digest)
            self.assertEqual(archive.with_suffix(".zip.sha256").read_text(),
                             f"{digest}  {archive.name}\n")
            with zipfile.ZipFile(archive) as zipped:
                for name in zipped.namelist():
                    self.assertFalse(name.startswith(("QA/", "scripts/", "docs/", ".git/")))
                    self.assertEqual(record["files"][name],
                                     hashlib.sha256(zipped.read(name)).hexdigest())
                self.assertEqual(json.loads(zipped.read("plugin.json"))["version"], record["version"])
            self.assertEqual(package.main(["--verify", str(archive)]), 0)
            self.assertEqual(record["host_acceptance"], "untested")


class ReleaseGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.run_git("init", "-q")
        self.run_git("config", "user.email", "release-test@example.invalid")
        self.run_git("config", "user.name", "Release test")
        self.source = self.root / "plugin.json"
        self.source.write_text('{"version":"1.2.3"}')
        (self.root / ".gitignore").write_text("ignored.md\n")
        self.run_git("add", ".")
        self.run_git("commit", "-qm", "fixture")
        self.run_git("tag", "-a", "v1.2.3", "-m", "fixture release")
        self.root_patch = patch.object(package, "ROOT", self.root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)

    def run_git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.root), *args], text=True)

    def check(self, tag="v1.2.3", files=None):
        package.check_release("1.2.3", tag, package.source_state(), files or [self.source])

    def test_clean_annotated_tag_accepted(self):
        self.check()

    def test_wrong_version_tag_rejected(self):
        with self.assertRaisesRegex(ValueError, "Release tag must be"):
            self.check("v9.9.9")

    def test_missing_tag_rejected(self):
        self.run_git("tag", "-d", "v1.2.3")
        with self.assertRaises(subprocess.CalledProcessError):
            self.check()

    def test_dirty_and_untracked_files_rejected(self):
        for staged in (False, True):
            self.source.write_text('{"version":"changed"}')
            if staged:
                self.run_git("add", "plugin.json")
            with self.assertRaisesRegex(ValueError, "clean checkout"):
                self.check()

    def test_untracked_file_rejected(self):
        (self.root / "untracked").write_text("text")
        with self.assertRaisesRegex(ValueError, "clean checkout"):
            self.check()

    def test_tag_at_other_commit_rejected(self):
        self.run_git("commit", "--allow-empty", "-qm", "next")
        with self.assertRaisesRegex(ValueError, "checked-out commit"):
            self.check()

    def test_ignored_package_input_rejected(self):
        ignored = self.root / "ignored.md"
        ignored.write_text("untracked payload")
        with self.assertRaisesRegex(ValueError, "Untracked or ignored"):
            self.check(files=[self.source, ignored])

    def test_hidden_tracked_modification_rejected(self):
        self.run_git("update-index", "--assume-unchanged", "plugin.json")
        self.source.write_text("modified but hidden from status")
        with self.assertRaisesRegex(ValueError, "differs from committed bytes"):
            self.check()


if __name__ == "__main__":
    unittest.main()
