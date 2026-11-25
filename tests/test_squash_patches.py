"""Exercise the patch application approval gate in isolated jj repositories."""

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "skills/jj-patch-stack/scripts/squash_patches.py"
JJ = shutil.which("jj")


@unittest.skipUnless(JJ, "requires jj")
class SquashWorkspaceTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="squash-workspaces-")
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.repo = self.directory / "task"
        config = self.directory / "jj.toml"
        config.write_text(
            '[user]\nname = "Workspace Fixture"\nemail = "fixture@example.invalid"\n'
            '[signing]\nbehavior = "drop"\n',
            encoding="utf-8",
        )
        self.env = {
            **os.environ,
            "JJ_CONFIG": str(config),
            # Reproduce redirected Python output on a Windows runner.
            "PYTHONIOENCODING": "cp1252",
        }
        self.jj("git", "init", str(self.repo), cwd=self.directory)
        (self.repo / "target.txt").write_text("target\n", encoding="utf-8")
        self.jj("commit", "-m", "target")
        self.target = self.commit_id("@-")
        (self.repo / "fix.txt").write_text("fix\n", encoding="utf-8")
        self.jj("commit", "-m", "patch 雪")
        self.patch = self.commit_id("@-")
        self.pair = f"{self.patch}:{self.target}"

    def run_command(self, command, *args, cwd=None):
        return subprocess.run(
            [command, *args], cwd=cwd or self.repo, env=self.env,
            capture_output=True, encoding="utf-8", timeout=30,
        )

    def success(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout.strip()

    def jj(self, *args, cwd=None):
        return self.success(self.run_command(JJ, "--no-pager", *args, cwd=cwd))

    def commit_id(self, revision):
        return self.jj("--ignore-working-copy", "log", "--no-graph", "-r", revision, "-T", "commit_id")

    def operation_id(self):
        return self.jj("--ignore-working-copy", "op", "log", "--limit", "1", "--no-graph", "-T", "id")

    def squash(self, *args):
        return self.run_command(sys.executable, "-B", str(SCRIPT), *args, self.pair)

    def workspace(self, name, parent):
        parent = self.commit_id(parent)
        checkout = self.directory / name
        self.jj("workspace", "add", "--name", name, "-r", parent, str(checkout))
        checkout_parent = self.jj("-R", str(checkout), "log", "--no-graph", "-r", "@-", "-T", "commit_id")
        self.assertEqual(checkout_parent, parent)
        return checkout

    def test_apply_requires_each_affected_workspace(self):
        pending = self.workspace("pending", self.target)
        (pending / "side.txt").write_text("uncommitted side work\n", encoding="utf-8")
        self.workspace("review", self.patch)
        self.workspace("unaffected", "root()")
        protected = self.commit_id("pending@")
        review = self.commit_id("review@")
        unaffected = self.commit_id("unaffected@")
        operation = self.operation_id()
        preview = self.success(self.squash())
        self.assertIn(f"Preview at operation {operation}", preview)
        self.assertIn("Other affected workspaces: 'pending', 'review'", preview)

        denied = self.squash("--apply", operation, "--allow-workspace", "review")
        self.assertNotEqual(denied.returncode, 0)
        self.assertIn("without approval: 'pending'", denied.stderr)
        self.assertEqual(self.operation_id(), operation)
        self.assertEqual(self.commit_id("pending@"), protected)
        self.assertEqual(self.commit_id("review@"), review)

        self.success(self.squash("--apply", operation, "--allow-workspace", "pending",
                                 "--allow-workspace", "review"))
        self.assertNotEqual(self.commit_id("pending@"), protected)
        self.assertNotEqual(self.commit_id("review@"), review)
        self.assertEqual(self.commit_id("unaffected@"), unaffected)
        self.assertEqual((pending / "side.txt").read_text(encoding="utf-8"), "uncommitted side work\n")

    def test_apply_in_task_workspace_needs_no_workspace_option(self):
        operation = self.operation_id()
        preview = self.success(self.squash())
        self.assertIn(f"Preview at operation {operation}", preview)
        self.assertIn("patch 雪", preview)
        self.assertNotIn("Other affected workspaces", preview)
        self.success(self.squash("--apply", operation))
        self.assertEqual((self.repo / "fix.txt").read_text(encoding="utf-8"), "fix\n")

    def test_shared_task_head_still_requires_other_workspaces_approval(self):
        shared = self.workspace("shared", self.patch)
        task_head = self.commit_id("@")
        self.jj("-R", str(shared), "edit", task_head)
        self.assertEqual(self.commit_id("shared@"), task_head)
        operation = self.operation_id()
        self.assertIn("Other affected workspaces: 'shared'", self.success(self.squash()))

        denied = self.squash("--apply", operation)
        self.assertNotEqual(denied.returncode, 0)
        self.assertIn("without approval: 'shared'", denied.stderr)
        self.assertEqual(self.commit_id("shared@"), task_head)
