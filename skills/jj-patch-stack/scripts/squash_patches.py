#!/usr/bin/env python3
"""Preview or apply reviewed, conflict-free Jujutsu patch pairs."""

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass


def jj(*args: str) -> str:
    return subprocess.run(
        ["jj", "--no-pager", *args], check=True, stdout=subprocess.PIPE, encoding="utf-8"
    ).stdout.strip()


def commits(revset: str) -> str:
    return jj("log", "--no-graph", "-r", revset, "-T", 'commit_id ++ "\\n"')


@dataclass(frozen=True)
class Revision:
    change: str
    commit: str

    @property
    def ref(self) -> str:
        return f"change_id({self.change})"


def resolve(revset: str) -> Revision:
    ids = jj("log", "--no-graph", "-r", f"exactly({revset}, 1)", "-T", 'change_id ++ " " ++ commit_id')
    return Revision(*ids.split())


def reviewed_revision(commit: str) -> Revision:
    if not re.fullmatch(r"[0-9a-f]+", commit):
        raise ValueError("Use full commit IDs in each PATCH_COMMIT:TARGET_COMMIT pair.")
    revision = resolve(f"commit_id({commit})")
    if revision.commit != commit or resolve(revision.ref) != revision:
        raise ValueError(f"Commit {commit} is abbreviated or no longer current.")
    return revision


def require_clean_working_copy() -> None:
    if not commits("@ & empty() ~ conflicts()"):
        raise ValueError("The working copy must be empty and conflict-free.")


def operation_id() -> str:
    return jj("op", "log", "--limit", "1", "--no-graph", "-T", "id")


def preflight(arguments: list[str]) -> list[tuple[Revision, Revision]]:
    pairs = []
    for argument in arguments:
        patch_id, separator, target_id = argument.partition(":")
        if not separator:
            raise ValueError("Use PATCH_COMMIT:TARGET_COMMIT for each pair.")
        pairs.append((reviewed_revision(patch_id), reviewed_revision(target_id)))

    patches = {patch.change for patch, _ in pairs}
    targets = {target.change for _, target in pairs}
    if len(patches) != len(pairs) or patches & targets:
        raise ValueError("Each patch must appear once and cannot be a destination.")

    for patch, target in pairs:
        if not commits(f"{target.ref} & ::{patch.ref}"):
            raise ValueError(f"Target {target.commit} must be an ancestor of patch {patch.commit}.")
        if commits(f"{patch.ref} & empty()"):
            raise ValueError(f"Patch {patch.commit} is empty.")

    for (previous_patch, previous_target), (patch, target) in zip(pairs, pairs[1:]):
        if not commits(f"{previous_target.ref} & ::{target.ref}") or not commits(
            f"{previous_patch.ref} & ::{patch.ref}"
        ):
            raise ValueError("Supply the target stack and its cumulative patches oldest first.")
    return pairs


def apply(pairs: list[tuple[Revision, Revision]], affected: str) -> None:
    for index, (patch, target) in enumerate(pairs):
        current_patch = resolve(patch.ref)
        resolve(target.ref)
        if commits(f"{patch.ref} & empty()"):
            raise ValueError(f"Patch {current_patch.commit} became empty after an earlier squash.")

        print(f"Squashing {patch.change} into {target.change}", flush=True)
        output = jj("squash", "--from", patch.ref, "--into", target.ref, "--use-destination-message")
        if output:
            print(output)
        if commits(f"conflicts() & {affected}"):
            raise ValueError("A squash introduced a conflict in the affected history.")

        if index + 1 == len(pairs) or pairs[index + 1][1] != target:
            reviewed_tree = f"commit_id({patch.commit})"
            if jj("diff", "--from", reviewed_tree, "--to", target.ref, "--summary"):
                raise ValueError(f"Target {target.change} differs from its reviewed patch tree.")
            print(f"Verified {target.change} at {resolve(target.ref).commit}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pairs", nargs="+", metavar="PATCH_COMMIT:TARGET_COMMIT")
    parser.add_argument("--apply", metavar="REVIEWED_OPERATION", help="apply after reviewing the preview")
    args = parser.parse_args()
    try:
        require_clean_working_copy()
        before = operation_id()
        if args.apply is not None and args.apply != before:
            raise ValueError("The repository operation changed. Review a new preview before applying.")
        pairs = preflight(args.pairs)
        affected = f"{pairs[0][1].ref}::"
        if commits(f"{affected} & (conflicts() | immutable())"):
            raise ValueError("The affected history must be conflict-free and mutable.")
        if operation_id() != before:
            raise ValueError("The repository operation changed during preflight. Review a new preview.")

        if args.apply is None:
            print(f"Preview at operation {before}")
            for patch, target in pairs:
                print(f"  {patch.change} ({patch.commit}) -> {target.change} ({target.commit})")
            print(jj("log", "-r", affected))
        else:
            print(f"Starting operation for recovery: {before}", flush=True)
            try:
                apply(pairs, affected)
            except (subprocess.CalledProcessError, ValueError):
                print("Stopped. Inspect the current operation before retrying. Earlier squashes may remain.", file=sys.stderr)
                raise
    except (OSError, subprocess.CalledProcessError, ValueError) as error:
        print(f"squash_patches: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
