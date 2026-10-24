"""Collect immutable Git evidence; leave semantic feature recognition to the caller."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys


class EvidenceError(Exception):
    """The requested evidence cannot be collected completely."""


REPOSITORY_ENVIRONMENT = {
    "GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GIT_IMPLICIT_WORK_TREE",
    "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_INDEX_FILE",
    "GIT_PREFIX", "GIT_GRAFT_FILE", "GIT_SHALLOW_FILE", "GIT_NAMESPACE",
    "GIT_REPLACE_REF_BASE", "GIT_ATTR_SOURCE",
}


class Git:
    def __init__(self, repository: Path):
        self.repository = repository.resolve()
        self.environment = {
            # --repo owns repository selection, even when called from a Git hook.
            **{key: value for key, value in os.environ.items()
               if key.upper() not in REPOSITORY_ENVIRONMENT},
            "GIT_OPTIONAL_LOCKS": "0",
            "GIT_NO_REPLACE_OBJECTS": "1",
        }
        self.repository = Path(self.run("rev-parse", "--show-toplevel").decode().strip())

    def run(self, *arguments: str, allow_no_match: bool = False,
            attribute_source: str | None = None) -> bytes:
        options = [f"--attr-source={attribute_source}"] if attribute_source else []
        result = subprocess.run(
            ["git", "--no-pager", "-C", str(self.repository), *options, *arguments],
            env=self.environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60,
            check=False,
        )
        if result.returncode != 0:
            if allow_no_match and result.returncode == 1:
                return b""
            detail = result.stderr.decode("utf-8", errors="replace").strip()
            raise EvidenceError(f"git {arguments[0]} failed: {detail}")
        return result.stdout

    def revision(self, revision: str) -> str:
        return self.run(
            "rev-parse", "--verify", "--end-of-options", f"{revision}^{{commit}}"
        ).decode("ascii").strip()

    def tree(self, revision: str) -> list[dict[str, str]]:
        entries = []
        for record in self.run("ls-tree", "-r", "-z", "--full-tree", revision).split(b"\0"):
            if not record:
                continue
            metadata, filename = record.split(b"\t", 1)
            mode, kind, object_id = metadata.decode("ascii").split()
            entries.append({
                "path": filename.decode("utf-8", errors="surrogateescape"),
                "mode": mode,
                "kind": kind,
                "object_id": object_id,
            })
        return entries


DIFF_OPTIONS = (
    "--binary", "--full-index", "--no-color", "--no-ext-diff", "--no-textconv",
    "--no-renames", "--src-prefix=a/", "--dst-prefix=b/",
)


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def collect(repository: Path, base: str, tip: str, output: Path,
            terms: list[str], max_commits: int) -> dict[str, object]:
    if max_commits < 1:
        raise EvidenceError("--max-commits must be positive")
    if any(not term or "\n" in term or "\r" in term or "\0" in term for term in terms):
        raise EvidenceError("--term must be a nonempty, single-line literal")
    git = Git(repository)
    if git.run("rev-parse", "--is-shallow-repository").strip() != b"false":
        raise EvidenceError("Shallow history cannot establish complete source ancestry")
    base_id, tip_id = git.revision(base), git.revision(tip)
    git.run("merge-base", "--is-ancestor", base_id, tip_id)
    revisions = git.run(
        "rev-list", "--reverse", "--topo-order", f"--max-count={max_commits + 1}",
        f"{base_id}..{tip_id}",
    ).decode("ascii").splitlines()
    if len(revisions) > max_commits:
        raise EvidenceError("Stack exceeds --max-commits; narrow scope or raise the limit")

    # Resolve and validate scope before creating any output. Never overwrite a run.
    output = output.resolve()
    if output.exists():
        raise EvidenceError("--output must be a new directory")
    metadata = [
        Path(git.run("rev-parse", "--absolute-git-dir").decode().strip()).resolve(),
        Path(git.run("rev-parse", "--path-format=absolute", "--git-common-dir").decode().strip()).resolve(),
        (git.repository / ".jj").resolve(),
    ]
    if any(output.is_relative_to(folder) for folder in metadata):
        raise EvidenceError("--output must be outside repository metadata")
    output.mkdir(parents=True)
    manifest: dict[str, object] = {
        "schema_version": 1,
        "status": "incomplete",
        "repository": str(git.repository),
        "base": base_id,
        "tip": tip_id,
        "range": "base excluded, tip included; all reachable side branches included",
        "terms": terms,
        "commits": [],
        "limitations": [
            "Literal references are unclassified candidates, including tests and dead code.",
            "Missing matches do not exclude indirect or external consumers.",
            "Binary contents and submodule repositories require separate inspection.",
            "Renames appear as deletions/additions; semantic lineage needs inspection.",
            "Working-copy changes are excluded; no feature boundaries are inferred.",
        ],
    }
    write_json(output / "manifest.json", manifest)
    selected = set(revisions)
    commits = []
    for revision in dict.fromkeys([base_id, *revisions]):
        folder = output / revision
        folder.mkdir()
        parents = git.run("show", "-s", "--format=%P", revision).decode("ascii").split()
        record = {
            "id": revision,
            "parents": parents,
            "context_parents": [parent for parent in parents if parent not in selected],
            "subject": git.run("show", "-s", "--format=%s", revision).decode(
                "utf-8", errors="replace"
            ).rstrip("\r\n"),
            "directory": revision,
            "patches": [],
        }
        write_json(folder / "tree.json", git.tree(revision))
        if terms:
            patterns = [argument for term in terms for argument in ("-e", term)]
            matches = git.run(
                "grep", "--no-color", "--no-textconv", "-I", "-n", "-F",
                "--full-name", *patterns, revision, "--", allow_no_match=True,
                attribute_source=revision,
            )
            (folder / "consumer-candidates.txt").write_bytes(matches)
        if revision == base_id:
            manifest["base_context"] = record
            continue
        for index, parent in enumerate(parents):
            patch = f"parent-{index + 1}.patch"
            (folder / patch).write_bytes(git.run(
                "diff", *DIFF_OPTIONS, parent, revision, "--", attribute_source=revision,
            ))
            record["patches"].append({"parent": parent, "file": patch})
        if not parents:
            patch = "root.patch"
            (folder / patch).write_bytes(git.run(
                "diff-tree", "--root", "--no-commit-id", "-r", "-p",
                *DIFF_OPTIONS, revision, "--",
                attribute_source=revision,
            ))
            record["patches"].append({"parent": None, "file": patch})
        commits.append(record)
    (output / "net.patch").write_bytes(git.run(
        "diff", *DIFF_OPTIONS, base_id, tip_id, "--", attribute_source=tip_id,
    ))
    manifest["commits"] = commits
    manifest["status"] = "complete"
    write_json(output / "manifest.json", manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--base", required=True, help="Excluded ancestor, as a Git revision")
    parser.add_argument("--tip", required=True, help="Included tip, as a Git revision")
    parser.add_argument("--output", type=Path, required=True, help="New evidence directory")
    parser.add_argument("--term", action="append", default=[], help="Literal consumer search term")
    parser.add_argument("--max-commits", type=int, default=500)
    args = parser.parse_args()
    try:
        manifest = collect(args.repo, args.base, args.tip, args.output, args.term, args.max_commits)
    except (EvidenceError, OSError, subprocess.TimeoutExpired) as error:
        print(f"Evidence collection failed: {error}", file=sys.stderr)
        print("Any partial output is incomplete; choose a new directory to retry.", file=sys.stderr)
        return 1
    print(f"Collected pinned evidence: {args.output.resolve() / 'manifest.json'}")
    print(f"Range: {manifest['base']}..{manifest['tip']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
