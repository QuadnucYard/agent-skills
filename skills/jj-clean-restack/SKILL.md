---
license: MIT
name: jj-clean-restack
description: >
  Clean up a messy linear Jujutsu change stack into a separate, reviewable
  stack while preserving the original commits (pinned with a tag), existing
  refs, and the final tree. Use when fixups, mixed commits, poor ordering,
  or temporary history need to be reorganized without rewriting the existing
  stack.
---

# Clean A Jujutsu Stack

Produce a new stack with a coherent history. The original stack is evidence
and must remain reachable and identifiable by full commit ID, pinned with a
tag. Do not silently replace the user's branch, publish over it, or flatten a
merge history.

## Operating contract

- Establish explicit `BASE`, `OLD_TIP`, `ORIGINAL_TAG`, and `CLEAN_TAG`;
  never infer the tip from `@` alone.
- Record full commit IDs of the original range before any mutation.
- Pin the original tip and the clean tip with tags (`jj tag set`), never
  bookmarks: jj moves a bookmark automatically when its commit is rewritten,
  while a tag keeps pointing at the exact pinned commit.
- Do not always rebuild the whole stack or restore the whole final tree.
  Keep the longest initial prefix that needs no content, description, or
  ordering changes; grow the clean suffix from its last commit, immediately
  before the first divergence. Record this commit as `REBUILD_BASE` (use
  `BASE` when no prefix can be retained). If the entire stack is already
  clean, retain it and report that no rebuild is needed.
- Preserve the original graph first. Build the clean stack by duplicating
  one source revision at a time onto the growing clean tip, in the final
  order chosen during analysis. Never duplicate the whole range up front and
  reorder it afterwards; `jj rebase` is not part of this workflow. For
  tangled refactors, rebuild a clean stack from the final tree instead.
- Never directly edit a change this workflow created — the duplicated
  clean-stack commits and the new commits from a final-state rebuild. Once
  such a change exists, do not check it out with `jj edit` and modify it in
  place, and never move `@` onto it in order to change it. To alter its
  content, create a new change directly on top of it (`jj new <DUP>`), edit
  only inside that new change, verify it, then fold it in with
  `jj squash --from <FIX> --into <DUP>`: verification gates the rewrite and
  every intermediate state stays inspectable. Original-stack commits are
  untouchable regardless, and `jj edit` remains allowed for the read-only
  per-commit checks in
  [validation-and-recovery.md](references/validation-and-recovery.md).
- Every clean commit must be well formatted: each description follows the
  repository's commit-message convention with no leftover fixup, WIP, or
  placeholder wording (see "Descriptions" in
  [reconstruction.md](references/reconstruction.md)), and content the rebuild
  itself produces (conflict resolutions, split assemblies, new commits) passes
  the repository's formatter and linters. Reformatting preserved original
  content changes the tree, so it needs the same explicit approval as any
  content change.
- Preserve the final tree exactly unless the user explicitly approves content
  changes.
- Keep existing bookmarks and tags unchanged; only ever create new tags.
- Stop on ambiguity, an unexpected merge, a commit-ID intersection outside the retained prefix, a tree
  mismatch, or an unexplained conflict.
- Format every command, flag, revset, revision expression, and change or
  commit ID as code: inline backticks in prose, fenced `sh` blocks for
  command sequences. Never leave code unformatted.
- Never use `--ignore-immutable` as a workaround.

The workflow is staged: inspect and freeze scope, analyze intent, build the
duplicate stack one commit at a time, transform, validate, then report.
Read detail as needed:

- [Scope and safety](references/scope-and-safety.md) before duplication and
  before every mutating command.
- [Reconstruction tactics](references/reconstruction.md) when choosing a
  reconstruction mode, classifying changes, splitting, folding, or using
  additive/subtractive operations.
- [Validation and recovery](references/validation-and-recovery.md) after
  transformation and whenever an invariant fails.

## Minimal workflow

1. Resolve the named revisions and inspect the graph. Confirm the range is
   the intended linear stack and record full commit IDs outside the
   repository when practical.
2. Pin the original tip with the safety tag `ORIGINAL_TAG`; never move or
   delete an existing tag or bookmark.
3. Analyze every commit by diff and dependency, not by subject alone. Decide
   whether boundaries are reusable or whether the stack is a refactor/tangle
   that should be rebuilt from the final tree. Decide the final order of the
   clean commits here. Identify the longest unchanged prefix and record
   `REBUILD_BASE`; keep those original commits without duplication.
4. Choose one reconstruction mode. Duplicate-and-edit builds the clean stack
   one source revision at a time onto the current clean tip, in the final
   order decided in step 3. Final-state rebuild creates a new child of
   `REBUILD_BASE`, restores the original final tree into it, and partitions only the net
   change from there. Record the exact source-to-new mapping or restore
   operation.
5. Rebuild intent using the least manual operation that fits: squash exact
   fixups, absorb clearly distributed changes, split mixed commits, or
   create new commits from selected additions and removals. Inspect after
   each operation. If the build exposes a wrong order, adjust the build plan
   and continue building; do not reshuffle finished duplicates.
6. Rewrite descriptions only on duplicate/new revisions, following the
   repository's commit-message convention, so each clean commit states its
   final purpose rather than its cleanup history.
7. Pin the clean tip with `CLEAN_TAG`. Validate tree equivalence (unless an
   explicit content change was approved), conflicts, empties, descriptions,
   and every intermediate commit's checks. Verify original IDs, tag
   positions, unchanged retained-prefix IDs, suffix separation, and report
   evidence and caveats.

## Scope boundary

This skill is for a linear stack. If the range contains merges, unrelated
branches, generated artifacts requiring policy decisions, or a requested
content change, stop and get an explicit plan rather than silently
interpreting it as a restack.
