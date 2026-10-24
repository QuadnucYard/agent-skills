"""Behavioral checks for the standalone feature-recognition evidence collector."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SCRIPT = (Path(__file__).resolve().parents[1] / "skills" /
          "recognize-stack-features" / "scripts" / "stack_evidence.py")


@unittest.skipUnless(shutil.which("git"), "Git is required")
class EvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        sandbox = tempfile.TemporaryDirectory(prefix="stack-evidence-test-")
        self.addCleanup(sandbox.cleanup)
        self.sandbox = Path(sandbox.name)
        self.repo = self.sandbox / "repository"
        self.repo.mkdir()
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Evidence Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.write("app.py", "def login():\n    return 'expired'\n")
        self.base = self.commit("initial state")
        self.output = self.sandbox / "evidence"

    def git(self, *arguments: str) -> str:
        result = subprocess.run(
            ["git", "--no-pager", "-C", str(self.repo), *arguments],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
        )
        return result.stdout.decode("utf-8").strip()

    def write(self, path: str, content: str) -> None:
        file = self.repo / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(content, encoding="utf-8")

    def commit(self, message: str) -> str:
        self.git("add", "--all")
        # Only these isolated fixture commits use an unsigned test identity.
        self.git("-c", "commit.gpgsign=false", "commit", "-m", message)
        return self.git("rev-parse", "HEAD")

    def invoke(self, tip: str, *extra: str, base: str | None = None,
               environment: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), "--repo", str(self.repo),
             "--base", base or self.base, "--tip", tip,
             "--output", str(self.output), *extra],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False,
            env=environment,
        )

    def collect(self, tip: str, *extra: str, base: str | None = None) -> dict:
        result = self.invoke(tip, *extra, base=base)
        self.assertEqual(result.returncode, 0, result.stderr)
        manifest = json.loads((self.output / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["status"], "complete")
        return manifest

    def test_deferred_adoption_and_mixed_commit_have_separate_evidence(self) -> None:
        self.write("encoder.py", "def encode(value):\n    return str(value)\n")
        self.write("tests/test_encoder.py", "from encoder import encode\nassert encode(1) == '1'\n")
        early = self.commit("complete export")
        self.write("export.py", "from encoder import encode\ndef export(value):\n    return encode(value)\n")
        self.write("app.py", "def login():\n    return 'valid'\n")
        tip = self.commit("small cleanup")
        manifest = self.collect(tip, "--term", "encode", "--term", "missing-name")
        self.assertEqual(manifest["base"], self.base)
        self.assertEqual(manifest["tip"], tip)
        self.assertEqual([item["id"] for item in manifest["commits"]], [early, tip])
        early_matches = (self.output / early / "consumer-candidates.txt").read_text()
        self.assertIn("tests/test_encoder.py", early_matches)
        self.assertNotIn("export.py", early_matches)
        self.assertIn("export.py", (self.output / tip / "consumer-candidates.txt").read_text())
        mixed_patch = (self.output / tip / "parent-1.patch").read_text()
        self.assertIn("a/app.py", mixed_patch)
        self.assertIn("b/export.py", mixed_patch)
        tree = json.loads((self.output / tip / "tree.json").read_text())
        self.assertEqual({row["path"] for row in tree},
                         {"app.py", "encoder.py", "export.py", "tests/test_encoder.py"})

    def test_merges_keep_side_branches_context_and_each_parent(self) -> None:
        shared = self.base
        self.write("main-base.txt", "baseline\n")
        self.base = self.commit("selected base")
        self.write("main.txt", "main feature\n")
        main = self.commit("main path")
        self.git("checkout", "-b", "side", shared)
        self.write("side.txt", "side feature\n")
        side = self.commit("side path")
        self.git("checkout", "main")
        self.git("-c", "commit.gpgsign=false", "merge", "--no-ff", "side", "-m", "merge")
        tip = self.git("rev-parse", "HEAD")
        manifest = self.collect(tip)
        records = {row["id"]: row for row in manifest["commits"]}
        self.assertEqual(set(records), {main, side, tip})
        self.assertEqual(records[side]["context_parents"], [shared])
        self.assertEqual(records[tip]["parents"], [main, side])
        self.assertEqual(len(records[tip]["patches"]), 2)
        self.assertIn("b/side.txt", (self.output / tip / "parent-1.patch").read_text())
        self.assertIn("b/main.txt", (self.output / tip / "parent-2.patch").read_text())
        positions = {row["id"]: i for i, row in enumerate(manifest["commits"])}
        for row in records.values():
            for parent in row["parents"]:
                if parent in positions:
                    self.assertLess(positions[parent], positions[row["id"]])

    def test_net_zero_history_and_unchanged_callers_remain_visible(self) -> None:
        self.write("helper.py", "def helper():\n    return 'old'\n")
        self.write("consumer.py", "from helper import helper\nprint(helper())\n")
        self.base = self.commit("existing production path")
        self.write("temporary.py", "def compat():\n    return 'legacy'\n")
        introduced = self.commit("compatibility stage")
        (self.repo / "temporary.py").unlink()
        self.write("helper.py", "def helper():\n    return 'new'\n")
        tip = self.commit("remove compatibility and repair helper")
        manifest = self.collect(tip, "--term", "helper")
        self.assertEqual(len(manifest["commits"]), 2)
        self.assertIn("temporary.py", (self.output / introduced / "parent-1.patch").read_text())
        self.assertIn("temporary.py", (self.output / tip / "parent-1.patch").read_text())
        self.assertNotIn("temporary.py", (self.output / "net.patch").read_text())
        self.assertIn("consumer.py", (self.output / tip / "consumer-candidates.txt").read_text())
        self.assertNotIn("consumer.py", (self.output / "net.patch").read_text())

    def test_repository_state_is_preserved_and_working_edits_are_excluded(self) -> None:
        self.write("new.txt", "committed\n")
        tip = self.commit("feature")
        self.write("app.py", "uncommitted-secret\n")
        self.write("untracked.txt", "uncommitted-secret\n")
        state = lambda: (self.git("status", "--porcelain=v1"),
                         self.git("for-each-ref", "--format=%(refname) %(objectname)"),
                         self.git("symbolic-ref", "HEAD"), self.git("diff"),
                         self.git("diff", "--cached"))
        before = state()
        self.collect(tip, "--term", "uncommitted-secret")
        self.assertEqual(before, state())
        self.assertEqual((self.output / tip / "consumer-candidates.txt").read_bytes(), b"")
        self.assertNotIn("uncommitted-secret", (self.output / "net.patch").read_text())

    def test_invalid_scope_limits_and_existing_output_are_refused(self) -> None:
        self.write("one.txt", "one\n")
        one = self.commit("one")
        self.write("two.txt", "two\n")
        two = self.commit("two")
        result = self.invoke(two, "--max-commits", "1")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.output.exists())
        result = self.invoke(one, base=two)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.output.exists())
        result = self.invoke(two, "--term", "")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.output.exists())
        self.output.mkdir()
        sentinel = self.output / "sentinel"
        sentinel.write_text("preserve")
        result = self.invoke(two)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(self.output.iterdir()), [sentinel])
        self.assertEqual(sentinel.read_text(), "preserve")

    def test_empty_range_and_literal_option_like_term(self) -> None:
        self.write("literal.txt", "-n\n")
        tip = self.commit("literal pattern")
        manifest = self.collect(tip, "--term=-n", base=tip)
        self.assertEqual(manifest["commits"], [])
        self.assertEqual((self.output / "net.patch").read_bytes(), b"")
        self.assertIn("literal.txt", (self.output / tip / "consumer-candidates.txt").read_text())

    def test_root_on_unrelated_merge_branch_is_preserved(self) -> None:
        self.git("checkout", "--orphan", "unrelated")
        self.git("rm", "-r", "--cached", ".")
        (self.repo / "app.py").unlink()
        self.write("independent.txt", "external root\n")
        root = self.commit("unrelated root")
        self.git("checkout", "main")
        self.git("-c", "commit.gpgsign=false", "merge", "--allow-unrelated-histories",
                 "--no-ff", "unrelated", "-m", "merge unrelated root")
        tip = self.git("rev-parse", "HEAD")
        manifest = self.collect(tip)
        record = next(row for row in manifest["commits"] if row["id"] == root)
        self.assertEqual(record["parents"], [])
        self.assertEqual(record["patches"], [{"parent": None, "file": "root.patch"}])
        self.assertIn("external root", (self.output / root / "root.patch").read_text())

    def test_metadata_output_is_refused(self) -> None:
        for folder in (".git", ".jj"):
            self.output = self.repo / folder / "new-evidence"
            result = self.invoke(self.base)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("metadata", result.stderr)
            self.assertFalse(self.output.exists())

    def test_explicit_repository_overrides_inherited_git_directory(self) -> None:
        other = self.sandbox / "other-repository"
        other.mkdir()
        for arguments in (
            ["init", "-b", "main"],
            ["-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
             "-c", "commit.gpgsign=false", "commit", "--allow-empty", "-m", "other"],
        ):
            result = subprocess.run(["git", "-C", str(other), *arguments],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(result.returncode, 0, result.stderr.decode())
        environment = {
            **os.environ,
            "GIT_DIR": str(other / ".git"),
            "GIT_WORK_TREE": str(other),
        }
        result = self.invoke("HEAD", base="HEAD", environment=environment)
        self.assertEqual(result.returncode, 0, result.stderr)
        manifest = json.loads((self.output / "manifest.json").read_text(encoding="utf-8"))
        # Git expands Windows short paths; compare directory identity.
        self.assertTrue(self.repo.samefile(manifest["repository"]),
                        f"Expected {self.repo}, got {manifest['repository']}")

    def test_dirty_attributes_do_not_change_committed_evidence(self) -> None:
        self.write("app.py", "def login():\n    return 'valid'\n")
        tip = self.commit("repair login")
        self.write(".gitattributes", "*.py -diff\n")
        before = self.git("status", "--porcelain=v1")
        self.collect(tip)
        for patch in (self.output / "net.patch", self.output / tip / "parent-1.patch"):
            self.assertIn("-    return 'expired'", patch.read_text())
            self.assertIn("+    return 'valid'", patch.read_text())
        self.assertEqual(before, self.git("status", "--porcelain=v1"))

    def test_attributes_follow_each_selected_revision(self) -> None:
        self.write("app.py", "def login():\n    return 'one'\n")
        text = self.commit("text change")
        self.write(".gitattributes", "*.py -diff\n")
        self.write("app.py", "def login():\n    return 'two'\n")
        binary = self.commit("binary attribute")
        (self.repo / ".gitattributes").unlink()
        self.write("app.py", "def login():\n    return 'three'\n")
        tip = self.commit("text again")
        self.collect(tip)
        self.assertIn("+    return 'one'", (self.output / text / "parent-1.patch").read_text())
        self.assertIn("GIT binary patch", (self.output / binary / "parent-1.patch").read_text())
        self.assertIn("+    return 'three'", (self.output / tip / "parent-1.patch").read_text())


if __name__ == "__main__":
    unittest.main()
