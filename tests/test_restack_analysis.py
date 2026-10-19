"""Behavioral tests for the standalone Nu/Python skill resources."""

import base64
import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from collections.abc import Sequence
from typing import ClassVar, Literal, TypedDict, cast, overload


SKILL = Path(__file__).resolve().parents[1] / "skills" / "jj-plan-restack"
sys.path.insert(0, str(SKILL / "scripts"))
import hunk_lineage as lineage


def file(text: str | bytes | None, name: str = "code.txt", kind: str = "file",
         executable: bool = False) -> lineage.Snapshot:
    data = text.encode() if isinstance(text, str) else text
    return {"path": name, "kind": kind, "executable": executable,
            "content": base64.b64encode(data).decode() if data is not None else None,
            "issue": None}


def change(label: str, old: str | bytes, new: str | bytes, name: str = "code.txt",
           status: str = "modified", new_name: str | None = None) -> lineage.Change:
    return {"change": label, "description": label,
            "entries": [{"status": status, "before": file(old, name),
                         "after": file(new, new_name or name)}]}


def analyze(*changes: lineage.Change, mode: lineage.AnalysisMode = "touches",
            path: str | None = None, hunk: str | None = None) -> lineage.AnalysisReport:
    request: lineage.AnalysisRequest = {
        "mode": mode, "base": "base", "tip": changes[-1]["change"],
        "changes": copy.deepcopy(list(changes)),
        "path": path, "hunk": hunk,
    }
    return lineage.analyze(request)


class LineageTests(unittest.TestCase):
    def test_offsets_shift_through_unrelated_edits(self) -> None:
        old = "alpha\nbeta\ngamma\ndelta\n"
        source = old.replace("beta", "chosen")
        shifted = "header\n" + source
        report = analyze(change("source", old, source),
                         change("shift", source, shifted),
                         change("fix", shifted, shifted.replace("chosen", "corrected")))
        self.assertTrue(report["complete"])
        self.assertEqual([(e["later"], e["relation"]) for e in report["events"]],
                         [("shift", "same-file"), ("fix", "overlap")])
        self.assertEqual(report["events"][-1]["before"], {"start": 3, "count": 1})
        self.assertNotIn("internal-", json.dumps(report))

    def test_multiple_hunks_can_be_selected(self) -> None:
        source = change("source", "a\nb\nc\nd\ne\n", "A\nb\nc\nd\nE\n")
        later = change("later", "A\nb\nc\nd\nE\n", "AA\nb\nc\nd\nE\n")
        report = analyze(source, later, hunk="h2")
        self.assertEqual(len(report["hunks"]), 1)
        self.assertEqual(report["events"][0]["relation"], "same-file")
        self.assertFalse(report["dependencies"])
        with self.assertRaisesRegex(ValueError, "--hunk"):
            analyze(source, later, hunk="h999")

    def test_replacement_and_revert_are_both_recorded(self) -> None:
        report = analyze(change("source", "old\n", "chosen\n"),
                         change("fix", "chosen\n", "fixed\n"),
                         change("revert", "fixed\n", "chosen\n"))
        self.assertEqual([e["later"] for e in report["events"] if e["relation"] == "overlap"],
                         ["fix", "revert"])

    def test_deletion_tombstone_tracks_later_insertion(self) -> None:
        report = analyze(change("delete", "a\nremoved\nz\n", "a\nz\n"),
                         change("restore", "a\nz\n", "a\nreplacement\nz\n"))
        self.assertEqual(report["hunks"][0]["after"]["count"], 0)
        self.assertEqual(report["events"][0]["relation"], "overlap")

    def test_adjacent_insertion_is_not_direct_overlap(self) -> None:
        report = analyze(change("source", "a\nb\nc\n", "a\nB\nc\n"),
                         change("adjacent", "a\nB\nc\n", "a\ninsert\nB\nc\n"))
        self.assertEqual(report["events"][0]["relation"], "adjacent")
        self.assertFalse(report["dependencies"])

    def test_recorded_rename_follows_path(self) -> None:
        report = analyze(change("source", "a\nb\n", "a\nB\n"),
                         change("rename", "a\nB\n", "a\nB\n", status="renamed", new_name="moved.txt"),
                         change("fix", "a\nB\n", "a\nC\n", name="moved.txt"))
        self.assertTrue(any(e["relation"] == "rename" for e in report["events"]))
        self.assertEqual(report["events"][-1]["relation"], "overlap")
        self.assertEqual(report["events"][-1]["path"], "moved.txt")

    def test_repeated_text_is_explicitly_uncertain(self) -> None:
        report = analyze(change("source", "old\nx\n", "same\nx\n"),
                         change("repeat", "same\nx\n", "same\nx\nsame\n"))
        self.assertFalse(report["complete"])
        self.assertIn("repeated", report["issues"][0]["reason"])

    def test_deleted_lineage_and_copies_require_review(self) -> None:
        for later in [change("delete", "a\nB\n", "a\n"),
                      change("copy", "a\nB\n", "a\nB\n", status="copied", new_name="copy.txt")]:
            with self.subTest(later=later["change"]):
                report = analyze(change("source", "a\nb\n", "a\nB\n"), later)
                self.assertFalse(report["complete"])

    def test_binary_non_utf8_and_non_regular_files_are_not_silently_skipped(self) -> None:
        for payload in [b"\0binary", b"\xff"]:
            report = analyze(change("source", b"old", payload))
            self.assertFalse(report["complete"])
        source = change("source", "old", "new")
        source["entries"][0]["after"]["kind"] = "symlink"
        self.assertFalse(analyze(source)["complete"])

    def test_unavailable_snapshot_does_not_reuse_stale_offsets(self) -> None:
        missing = change("missing", "a\nB\n", "a\nB\n")
        missing["entries"][0]["after"]["issue"] = "file exceeds limit"
        report = analyze(change("source", "a\nb\n", "a\nB\n"), missing,
                         change("later", "a\nB\n", "a\nC\n"))
        self.assertFalse(report["complete"])
        self.assertEqual(report["events"][-1]["relation"], "uncertain")

    def test_line_endings_and_missing_final_newline_are_changes(self) -> None:
        report = analyze(change("source", b"a\r\nb\r\n", b"a\r\nB\r\n"),
                         change("newline", b"a\r\nB\r\n", b"a\r\nB"))
        self.assertEqual(report["events"][0]["relation"], "overlap")

    def test_dependencies_include_each_original_owner(self) -> None:
        report = analyze(change("one", "a\n", "b\n"),
                         change("two", "b\n", "c\n"),
                         change("three", "c\n", "d\n"), mode="dependencies")
        self.assertEqual({(e["prerequisite"], e["dependent"]) for e in report["dependencies"]},
                         {("one", "two"), ("one", "three"), ("two", "three")})

    def test_metadata_only_source_does_not_own_later_text_edits(self) -> None:
        metadata = change("mode", "a\nb\n", "a\nb\n")
        metadata["entries"][0]["after"]["executable"] = True
        report = analyze(metadata, change("text", "a\nb\n", "a\nB\n"))
        self.assertEqual(report["hunks"][0]["kind"], "metadata")
        self.assertFalse(report["dependencies"])
        self.assertEqual(report["events"][0]["relation"], "same-file")

    def test_empty_file_creation_is_a_path_prerequisite(self) -> None:
        added = change("create", "", "", status="added")
        added["entries"][0]["before"]["kind"] = "absent"
        report = analyze(added, change("text", "", "new\n"))
        self.assertEqual(report["hunks"][0]["kind"], "path")
        self.assertEqual(report["dependencies"][0]["evidence"], "path")

    def test_nonempty_file_creation_remains_a_prerequisite_for_appends(self) -> None:
        added = change("create", "", "first\n", status="added")
        added["entries"][0]["before"]["kind"] = "absent"
        report = analyze(added, change("append", "first\n", "first\nsecond\n"))
        self.assertTrue(any(edge["evidence"] == "path" for edge in report["dependencies"]))

    def test_rename_with_text_edits_remains_a_path_prerequisite(self) -> None:
        renamed = change("rename", "a\nb\n", "A\nb\n", status="renamed", new_name="new.txt")
        report = analyze(renamed, change("append", "A\nb\n", "A\nb\nc\n", name="new.txt"))
        self.assertTrue(any(edge["evidence"] == "path" for edge in report["dependencies"]))

    def test_resource_budget_is_reported_without_running_unbounded_diff(self) -> None:
        report = analyze(change("large", "a\n" * 5001, "b\n" * 5001))
        self.assertFalse(report["complete"])
        self.assertIn("budget", report["issues"][0]["reason"])

    def test_unicode_separators_do_not_change_lf_line_numbers(self) -> None:
        report = analyze(change("source", "a\u2028b\nz\n", "a\u2028B\nz\n"))
        self.assertEqual(report["hunks"][0]["after"], {"start": 1, "count": 1})


    def test_cross_file_extraction_is_flagged_without_guessing_entity_identity(self) -> None:
        source = change("source", "head\nold\nend\n", "head\nchosen\nend\n")
        extraction = change("extract", "head\nchosen\nend\n", "head\ncall helper\nend\n")
        addition = change("extract", "", "chosen\n", name="helper.txt", status="added")
        addition["entries"][0]["before"]["kind"] = "absent"
        extraction["entries"].extend(addition["entries"])
        report = analyze(source, extraction, change("fix", "chosen\n", "fixed\n", name="helper.txt"))
        self.assertFalse(report["complete"])
        self.assertIn("helper.txt", report["issues"][0]["reason"])


class CheckEvent(TypedDict):
    change: str
    description: str
    path: str
    source_path: str
    status: Literal["clean", "conflict", "unknown"]
    reason: str


class CheckReport(TypedDict):
    status: Literal["clean", "conflict", "unknown"]
    complete: bool
    events: list[CheckEvent]
    reordered_dependencies: list[lineage.Dependency]
    unassessed: list[str]
    source_conflicts: list[dict[str, str]]


class StandaloneCliTests(unittest.TestCase):
    jj: ClassVar[str]
    nu: ClassVar[str]

    @classmethod
    def setUpClass(cls) -> None:
        cls.jj = os.environ.get("RESTACK_JJ") or shutil.which("jj") or ""
        cls.nu = os.environ.get("RESTACK_NU") or shutil.which("nu") or ""
        if not cls.jj or not cls.nu or not shutil.which("git"):
            raise RuntimeError("Analysis integration tests require jj, nu, git, and Python 3")

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="restack analysis ")
        self.addCleanup(self.temporary.cleanup)
        self.home = Path(self.temporary.name)
        self.repo = self.home / "repo"
        # Run copied skill resources outside the checkout, without node_modules or package files.
        self.installed = self.home / "installed skill"
        shutil.copytree(SKILL / "scripts", self.installed)
        config = self.home / "user.toml"
        config.write_text('[user]\nname="Analysis Fixture"\nemail="fixture@example.invalid"\n'
                          '[signing]\nbehavior="drop"\n[ui]\neditor=["must-not-launch"]\n')
        self.env = {**os.environ, "JJ_CONFIG": str(config), "PYTHONDONTWRITEBYTECODE": "1"}
        self.call([self.jj, "--no-pager", "git", "init", str(self.repo)], cwd=self.home)

    def call(self, args: Sequence[str], cwd: Path | None = None,
             check: bool = True) -> subprocess.CompletedProcess[bytes]:
        result = subprocess.run(args, cwd=cwd or self.repo, env=self.env,
                                capture_output=True, timeout=60)
        if check:
            self.assertEqual(result.returncode, 0,
                             result.stdout.decode(errors="replace") + result.stderr.decode(errors="replace"))
        return result

    def jjrun(self, *args: str) -> str:
        return self.call([self.jj, "--no-pager", *args]).stdout.decode().strip()

    def write(self, text: str | bytes, name: str = "code.txt") -> None:
        target = self.repo / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(text.encode() if isinstance(text, str) else text)

    def commit(self, text: str | bytes, description: str, name: str = "code.txt") -> str:
        self.write(text, name)
        self.jjrun("describe", "-m", description)
        revision = self.jjrun("log", "--no-graph", "-r", "@", "-T", "change_id")
        self.jjrun("new", "-m", "Next fixture")
        return revision

    @overload
    def cli(self, script: Literal["analyze-history.nu"], *args: str,
            check: Literal[True] = True) -> lineage.AnalysisReport: ...

    @overload
    def cli(self, script: Literal["check-restack.nu"], *args: str,
            check: Literal[True] = True) -> CheckReport: ...

    @overload
    def cli(self, script: str, *args: str,
            check: Literal[False]) -> subprocess.CompletedProcess[bytes]: ...

    def cli(self, script: str, *args: str, check: bool = True
            ) -> lineage.AnalysisReport | CheckReport | subprocess.CompletedProcess[bytes]:
        result = self.call([self.nu, "--no-config-file", str(self.installed / script),
                            *args, "--repository", str(self.repo), "--jj", self.jj,
                            "--python", sys.executable, "--json"], check=check)
        if not check:
            return result
        if script == "analyze-history.nu":
            return cast(lineage.AnalysisReport, json.loads(result.stdout))
        return cast(CheckReport, json.loads(result.stdout))

    def original_state(self) -> tuple[dict[str, bytes], list[str], bytes]:
        files = {str(p.relative_to(self.repo)): p.read_bytes() for p in self.repo.rglob("*")
                 if p.is_file() and ".git" not in p.parts and ".jj" not in p.parts}
        heads = self.repo / ".jj" / "repo" / "op_heads" / "heads"
        return files, sorted(p.name for p in heads.iterdir()), (self.repo / ".jj" / "working_copy" / "checkout").read_bytes()

    def test_later_hunk_touch_with_dirty_worktree_preserves_all_state(self) -> None:
        name = "odd (x) [y] & 雪.txt"
        base = self.commit("a\nb\nc\nd\n", "Base", name)
        source = self.commit("a\nB\nc\nd\n", "Interested feature", name)
        self.commit("header\na\nB\nc\nd\n", "Shift unrelated lines", name)
        tip = self.commit("header\na\nBB\nc\nd\n", "Correct the feature", name)
        self.jjrun("tag", "set", "original-fixture", "-r", tip)
        self.jjrun("bookmark", "create", "existing-fixture", "-r", tip)
        self.write("unsnapshotted work", "unrelated.txt")
        before = self.original_state()
        report = self.cli("analyze-history.nu", "touches", "--base", base, "--tip", tip,
                          "--change", source, "--path", name)
        self.assertTrue(report["complete"])
        self.assertEqual(report["events"][-1]["relation"], "overlap")
        self.assertEqual(report["events"][-1]["later"], tip[:12])
        self.assertEqual(before, self.original_state())
        self.assertEqual(self.jjrun("log", "--ignore-working-copy", "--no-graph", "-r", "original-fixture", "-T", "change_id"), tip)

    def test_order_checks_dependencies_and_stops_before_unassessed_descendants(self) -> None:
        base = self.commit("a\nb\nc\n", "Base")
        one = self.commit("a\nB\nc\n", "One")
        two = self.commit("a\nBB\nc\n", "Two")
        order = self.home / "order.json"
        order.write_text(json.dumps([two, one]))
        before = self.original_state()
        report = self.cli("check-restack.nu", "--base", base, "--tip", two, "--order", str(order))
        self.assertEqual(report["status"], "conflict")
        self.assertTrue(report["reordered_dependencies"])
        self.assertEqual(report["unassessed"], [one[:12]])
        self.assertEqual(before, self.original_state())
        order.write_text(json.dumps([one, two]))
        clean = self.cli("check-restack.nu", "--base", base, "--tip", two, "--order", str(order))
        self.assertEqual(clean["status"], "clean")
        self.assertTrue(clean["complete"])

    def test_whole_file_query_can_start_at_base_without_a_source_edit(self) -> None:
        base = self.commit("a\nb\nc\n", "Base")
        self.commit("other file\n", "Unrelated", "other.txt")
        tip = self.commit("a\nB\nc\n", "Later file edit")
        report = self.cli("analyze-history.nu", "touches", "--base", base, "--tip", tip,
                          "--change", base, "--path", "code.txt", "--whole-file")
        self.assertEqual(report["hunks"][0]["kind"], "whole-file")
        self.assertEqual(report["events"][0]["later"], tip[:12])
        self.assertEqual(report["events"][0]["relation"], "overlap")

    def test_empty_commits_are_assessed_in_an_ordered_stack(self) -> None:
        base = self.commit("base\n", "Base")
        empty = self.jjrun("log", "--no-graph", "-r", "@", "-T", "change_id")
        self.jjrun("new", "-m", "Next")
        tip = self.commit("changed\n", "Text edit")
        order = self.home / "order.json"
        order.write_text(json.dumps([empty, tip]))
        report = self.cli("check-restack.nu", "--base", base, "--tip", tip, "--order", str(order))
        self.assertEqual(report["status"], "clean")
        self.assertEqual(report["unassessed"], [])

    def test_three_way_merge_accepts_distant_edits_and_rejects_overlapping_edits(self) -> None:
        original = "".join(f"line {i}\n" for i in range(15))
        base = self.commit(original, "Base")
        source = self.commit(original.replace("line 2\n", "source 2\n"), "Source")
        self.jjrun("new", base, "-m", "Independent branch")
        destination = self.commit(original.replace("line 12\n", "destination 12\n"), "Destination")
        report = self.cli("check-restack.nu", "--change", source, "--onto", destination)
        self.assertEqual(report["status"], "clean")
        self.assertEqual(report["events"][0]["reason"], "three-way text merge")
        self.jjrun("new", base, "-m", "Conflicting branch")
        conflict = self.commit(original.replace("line 2\n", "other 2\n"), "Conflict")
        report = self.cli("check-restack.nu", "--change", source, "--onto", conflict)
        self.assertEqual(report["status"], "conflict")

    def test_add_delete_binary_and_missing_merger(self) -> None:
        base = self.commit("base\n", "Base")
        added = self.commit("source\n", "Add", "new.txt")
        report = self.cli("check-restack.nu", "--change", added, "--onto", base)
        self.assertEqual(report["status"], "clean")
        report = self.cli("check-restack.nu", "--change", added, "--onto", added)
        self.assertEqual(report["status"], "clean")
        self.jjrun("new", base, "-m", "Other addition")
        other = self.commit("other\n", "Other", "new.txt")
        self.assertEqual(self.cli("check-restack.nu", "--change", added, "--onto", other)["status"], "conflict")
        self.jjrun("new", base, "-m", "Deletion")
        (self.repo / "code.txt").unlink()
        deleted = self.jjrun("log", "--no-graph", "-r", "@", "-T", "change_id")
        self.assertEqual(self.cli("check-restack.nu", "--change", deleted, "--onto", base)["status"], "clean")
        self.jjrun("new", base, "-m", "Binary")
        binary = self.commit(b"\0binary", "Binary")
        self.assertEqual(self.cli("check-restack.nu", "--change", binary, "--onto", base)["status"], "unknown")
        self.jjrun("new", base, "-m", "Text one")
        source = self.commit("source\n", "Text one")
        self.jjrun("new", base, "-m", "Text two")
        target = self.commit("target\n", "Text two")
        report = self.cli("check-restack.nu", "--change", source, "--onto", target,
                          "--git", str(self.home / "missing-git"))
        self.assertEqual(report["status"], "unknown")

    def test_invalid_scope_and_limits_fail_explicitly(self) -> None:
        base = self.commit("a\n", "Base")
        one = self.commit("b\n", "One")
        two = self.commit("c\n", "Two")
        for extra in [("--max-commits", "1"), ("--change", "all()")]:
            result = self.cli("analyze-history.nu", "touches", "--base", base,
                              "--tip", two, *(extra if extra[0] == "--change" else ("--change", one, *extra)), check=False)
            self.assertNotEqual(result.returncode, 0)
        report = self.cli("analyze-history.nu", "touches", "--base", base, "--tip", two,
                          "--change", one, "--max-file-bytes", "1")
        self.assertFalse(report["complete"])
        order = self.home / "order.json"
        order.write_text(json.dumps([one, one]))
        self.assertNotEqual(self.cli("check-restack.nu", "--base", base, "--tip", two,
                                    "--order", str(order), check=False).returncode, 0)
        self.jjrun("new", one, two, "-m", "Merge")
        merge = self.jjrun("log", "--no-graph", "-r", "@", "-T", "change_id")
        self.assertNotEqual(self.cli("analyze-history.nu", "dependencies", "--base", base,
                                    "--tip", merge, check=False).returncode, 0)

    def test_file_directory_collisions_are_conflicts_at_commit_boundaries(self) -> None:
        base = self.commit("base\n", "Base")
        added_file = self.commit("file\n", "Add file", "tree")
        self.jjrun("new", base, "-m", "Other tree")
        added_child = self.commit("child\n", "Add child", "tree/child.txt")
        for source, destination in [(added_file, added_child), (added_child, added_file)]:
            report = self.cli("check-restack.nu", "--change", source, "--onto", destination)
            self.assertEqual(report["status"], "conflict")
            self.assertEqual(report["events"][-1]["reason"], "file/directory conflict")

    def test_inherited_source_conflicts_cannot_produce_a_clean_prediction(self) -> None:
        base = self.commit("base\n", "Base")
        one = self.commit("one\n", "One")
        self.jjrun("new", base, "-m", "Other side")
        two = self.commit("two\n", "Two")
        self.jjrun("new", one, two, "-m", "Conflicted merge")
        self.jjrun("new", "-m", "Inherit conflict")
        source = self.commit("other file\n", "Unrelated edit", "other.txt")
        report = self.cli("check-restack.nu", "--change", source, "--onto", base)
        self.assertEqual(report["status"], "unknown")
        self.assertFalse(report["complete"])
        self.assertEqual(report["source_conflicts"][0]["path"], "code.txt")


if __name__ == "__main__":
    unittest.main()
