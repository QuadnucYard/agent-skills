---
license: MIT
name: jj-clean-restack
description: >
  Clean up a messy linear Jujutsu change stack into a separate, reviewable
  stack while preserving the original commits (pinned with a tag), existing
  refs, incremental feature history, and the final tree. Reconstruct from
  commit intent and meaningful intermediate states; duplicate only a small,
  manually confirmed reusable slice. Use when fixups, mixed commits, poor
  ordering, or temporary history need to be reorganized without rewriting the
  existing stack.
---

# Clean A Jujutsu Stack

Produce a new stack with a coherent history. The original stack is evidence
and must remain reachable and internally identifiable by full commit ID,
pinned with a tag. Do not silently replace the user's branch, publish over it,
or flatten a merge history.

## Operating contract

- Establish explicit `BASE`, `OLD_TIP`, `ORIGINAL_TAG`, and `CLEAN_BOOKMARK`;
  never infer the tip from `@` alone.
- Record full commit IDs of the original range before any mutation.
- Pin the original tip with an immutable safety tag (`jj tag set`). Track the
  rebuilt tip with a newly created dedicated bookmark. Never use a bookmark as
  the original-stack safety reference, and never use a second tag for the
  rebuilt stack. Advance only `CLEAN_BOOKMARK`, and only after the new rebuilt
  tip passes its immediate manual validation; do not move any pre-existing
  bookmark or any tag.
- Do not always rebuild the whole stack or restore the whole final tree.
  Keep the longest initial prefix that needs no content, description, or
  ordering changes; grow the clean suffix from its last commit, immediately
  before the first divergence. Record this commit as `REBUILD_BASE` (use
  `BASE` when no prefix can be retained). If the entire stack is already
  clean, retain it and report that no rebuild is needed.
- Preserve the original graph first. Reconstruct the changed suffix from the
  original history's intent and meaningful intermediate states. The final tree
  is one source of evidence, not the default reconstruction source: it can hide
  incremental features, migrations, compatibility stages, and intentional
  removals. Duplication is an exceptional reuse tactic for a
  small, explicitly bounded source slice, never the mechanism for copying the
  original stack or the whole suffix. Before duplicating anything, manually
  inspect every commit in that slice and confirm that all or most of each
  commit belongs unchanged in one planned clean commit, with useful boundaries
  and valid dependencies. Record that evidence and the exact edits still
  needed. If the proposed slice is broad, uncertain, or collectively covers
  the original stack, do not duplicate it; reconstruct those changes from
  selected original diffs, milestone trees, and explicit edits. Never duplicate
  a range specifier or use `jj rebase` to arrange the result.
- Never directly edit a change this workflow created — the duplicated
  clean-stack commits and newly reconstructed commits. Once
  such a change exists, do not check it out with `jj edit` and modify it in
  place, and never move `@` onto it in order to change it. For a correction
  that belongs wholly to one rebuilt commit, create a new change on top, edit
  and verify there, then squash it into that one destination. A later change
  may instead contain hunks for several earlier rebuilt commits: map every
  hunk to its intended destination and use explicitly scoped absorption or
  splitting rather than forcing the whole change into one commit. Original
  stack commits are untouchable regardless, and `jj edit` remains allowed for
  the read-only per-commit checks in
  [validation-and-recovery.md](references/validation-and-recovery.md).
- Every rebuilt commit is a manual validation gate. Before building the next
  commit, inspect its complete diff against its actual clean parent, confirm
  its stated intent and dependencies, and run the relevant behavioral check.
  Reconstruct one planned commit at a time; do not accumulate several
  unchecked commits and validate them later.
  Automated summaries, tree equivalence, and tests do not replace reading the
  diff. A commit that has not passed this review must not remain in the clean
  stack or be reported as validated. Any later operation that rewrites an
  already validated commit invalidates that evidence: manually revalidate
  every rewritten destination and each affected descendant before continuing.
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
- Preserve every meaningful incremental state identified during analysis, even
  when later commits modify or remove it and the final tree no longer contains
  it. Final-tip tree equivalence is necessary but does not prove historical
  equivalence. Omit an intermediate state only after establishing that it was
  fixup noise, an invalid partial implementation, or otherwise not an intended
  reviewable feature boundary.
- Keep existing bookmarks and tags unchanged. Create only `ORIGINAL_TAG` and
  `CLEAN_BOOKMARK`; only the new clean bookmark may move as construction
  advances.
- Stop on ambiguity, an unexpected merge, a commit-ID intersection outside the retained prefix, a tree
  mismatch, or an unexplained conflict.
- Keep commit IDs/Git hashes internal. Never expose them in user-facing
  conversation, plans, tables, or reports. Identify every revision shown to
  the user with at least its short jj change ID (`change_id.short()`), plus its
  description and relevant tag/bookmark or original/clean role when needed to
  disambiguate it. Do not paste command output containing commit IDs; render a
  user-facing view that follows this rule instead.
- Format every command, flag, revset, revision expression, and change or
  commit ID as code: inline backticks in prose, fenced `sh` blocks for
  command sequences. Never leave code unformatted.
- Never use `--ignore-immutable` as a workaround.

The workflow is staged: inspect and freeze scope, analyze intent, reconstruct
the suffix in small slices, manually validate each rebuilt commit, validate
the complete result, then report.
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
2. Pin the original tip with the safety tag `ORIGINAL_TAG`. Reserve an unused
   `CLEAN_BOOKMARK` name; create it after the first rebuilt commit passes
   manual validation and keep it on the latest validated rebuilt tip. Never
   move or delete an existing tag or bookmark.
3. Analyze every commit by reading its complete diff and checking its
   dependencies, not by subject or summary alone. Decide the final clean
   boundaries and order. Build a semantic timeline of features, migrations,
   compatibility stages, deprecations, and removals; mark which intermediate
   states must remain visible even when absent from `OLD_TIP`. Identify the
   longest unchanged prefix and record
   `REBUILD_BASE`; keep those original commits without duplication. Mark any
   proposed duplicate slice explicitly and justify, commit by commit, that it
   is small and that each commit will be fully or mostly retained. Reject any
   plan that duplicates the whole original stack or uses duplication as the
   general reconstruction strategy. Before the first reconstruction mutation,
   present a concrete plan to the user with all three views defined in
   [reconstruction.md](references/reconstruction.md): what every original
   commit does, how all of its content and meaningful states will be
   redistributed, and the complete ordered shape of the clean stack. Use
   short jj change IDs, never commit IDs/Git hashes, in that plan. Do not hide
   an unresolved destination or dependency behind a high-level summary; stop
   for clarification when the plan cannot account for it confidently.
4. Rebuild the suffix one planned semantic milestone at a time, using selected
   original diffs, original milestone trees, and explicit edits. A confirmed
   small reusable slice may be duplicated one explicit revision at a time at
   its planned position. A final-state partition is allowed only after a
   commit-by-commit audit proves that no meaningful incremental state would be
   hidden; it is never the fallback merely because broad duplication is
   prohibited. Never restore content that is also going to be duplicated, and
   never pass a range to `jj duplicate`. Record every source milestone,
   restore operation, hunk destination, and source-to-new mapping.
5. Rebuild intent using the least manual operation that fits. Squash only when
   the entire source belongs to one destination. A later commit may be a
   distributed fixup for several earlier commits; map its hunks and absorb or
   split them into every correct destination rather than choosing one owner.
   Reconstruct one planned commit at a time. After creating or rewriting one
   rebuilt commit, stop and manually validate
   its full parent diff, intent, dependency completeness, and relevant behavior
   before continuing. When one operation rewrites multiple commits, manually
   validate each rewritten commit from oldest to newest and then every affected
   descendant. If the build exposes a wrong order, adjust the build plan; do
   not reshuffle finished duplicates.
6. Rewrite descriptions only on duplicate/new revisions, following the
   repository's commit-message convention, so each clean commit states its
   final purpose rather than its cleanup history.
7. Point `CLEAN_BOOKMARK` at `CLEAN_TIP`. Validate tree equivalence (unless an
   explicit content change was approved), conflicts, empties, descriptions,
   and the recorded manual review and checks for every rebuilt commit. Verify
   the rebuilt semantic timeline against every required original milestone;
   then verify original IDs, the original tag, the clean bookmark, unchanged
   retained-prefix IDs, suffix separation, and report evidence and caveats.

## Scope boundary

This skill is for a linear stack. If the range contains merges, unrelated
branches, generated artifacts requiring policy decisions, or a requested
content change, stop and get an explicit plan rather than silently
interpreting it as a restack.
