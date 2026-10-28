# Validation And Recovery

## Required validation

The clean tip must equal `EXPECTED_TIP`: the independently prepared extraction
target when features are excluded, otherwise `ORIGINAL_TIP`. `ORIGINAL_TIP` is
the corrected full source when fixes exist, otherwise the pre-fix source.

```sh
jj diff --from "$EXPECTED_TIP" --to "$CLEAN_TIP" --summary
jj diff --from "$EXPECTED_TIP" --to "$CLEAN_TIP" --git
```

With fixes or extraction, inspect the complete pre-fix-to-corrected,
corrected-to-target, and pre-fix-to-clean diffs. These must account separately
for authorized fixes, exclusions, and adaptations, with no unexplained hunks.
Check retained behavior and interactions and absence of excluded entry points.
Verify the target was prepared and validated independently of clean history;
matching a target copied from the rebuilt tip proves nothing. Never claim
equality to a full-source tree when extraction intentionally changes it.

Tip equivalence is necessary but insufficient. Compare the rebuilt sequence to
the semantic timeline recorded during analysis. Every meaningful incremental
feature, migration or compatibility stage, deprecation, and intentional
removal must appear at an appropriate clean commit, including states no longer
present in `OLD_TIP`. For every omitted original state, verify the recorded
finding that it was fixup noise, invalid partial work, an authorized feature
exclusion, or otherwise not an intended reviewable milestone.

Also require:

```sh
jj log -r "conflicts() & ($NEW_STACK)"
jj log -r "empty() & ($NEW_STACK)"
jj log -r "$NEW_STACK" --no-graph \
  -T 'commit_id.short() ++ " " ++ description.first_line() ++ "\\n"'
```

Conflicts must be absent. Empty commits need an intentional explanation.
Descriptions must not leave standalone `fix`, `fixup`, `wip`, `typo`, or
review-follow-up commits, and every description must be well formatted in the
repository's commit-message convention (see "Descriptions" in
`reconstruction.md`). Review every clean commit from oldest to newest:
inspect its diff, check parent dependencies, and run the narrowest relevant
build/test/type checks. Do not claim intermediate validity if a check was
not run or cannot be run.

This final pass confirms, but does not replace, the manual gate performed
immediately after each rebuilt commit was created. Every rebuilt slice must
have a recorded commit-by-commit review. There is no valid batch review of a
slice. If a later squash, absorb, split, or conflict resolution changes an
already reviewed commit's content or parent tree, its prior validation is stale;
repeat the full protocol for every affected commit and descendant before
continuing the rebuild. For description-only rewrites, prove unchanged content
and parent trees, record old-to-new exact identities, and recheck descriptions,
graph, and refs. Carry forward applicable behavior evidence explicitly; rerun
checks dependent on revision metadata or changed execution conditions. A new
commit hash alone does not invalidate content-based behavior evidence.

## Per-commit check protocol

For each clean commit, from oldest to newest:

1. Manually read the complete diff against the commit's actual clean parent;
   do not rely on `--stat`, summaries, tests, or tree equivalence as a proxy.
   Confirm that every hunk belongs to the stated purpose and that no expected
   hunk is missing.
2. Confirm every referenced symbol,
   schema, generated file, and test fixture is provided by the parent or the
   commit itself.
3. Confirm which semantic milestone the commit realizes and compare its tree
   and behavior with the relevant original milestone evidence. Exact trees need
   not match when boundaries were intentionally redesigned, but the capability
   and transition must be accounted for.
4. Check the commit at that revision in an isolated working state (for example
   with the repository's established `jj edit`/`jj new` workflow). The
   original tag pins the old tip and the clean bookmark identifies the rebuilt
   tip, so checking out an intermediate commit cannot lose either endpoint.
5. Run checks proportional to the change: focused unit tests first, then the
   relevant integration tests and build/type checks. Review behavior and design
   adoption; do not spend review on formatting or lint.
   A refactor must run behavior/regression tests, not only compilation.
6. Record the review conclusion, exact commands, and outcomes. A failed,
   skipped, or not-manually-reviewed commit blocks the next milestone and
   completion. Repair the owning commit and recheck affected descendants;
   a passing tip cannot excuse a broken intermediate commit.

At minimum, the oldest rebuilt commit must build against `REBUILD_BASE`; every
later commit must build against its immediate clean parent. Inspect the retained
prefix for unchanged IDs and coherent behavior, and report relevant existing
validation evidence or gaps. If a commit cannot be
validated independently, split it differently or keep it with the dependency
it requires.

Verify the original commit-ID list is unchanged, that `jj tag list` still
shows `ORIGINAL_TAG` on the recorded original tip, and that `jj bookmark list`
shows `CLEAN_BOOKMARK` on `CLEAN_TIP` when a clean bookmark was created. Inspect
the final graph and confirm the
clean stack is a separate suffix rooted at `REBUILD_BASE`. Its intersection
with the original range must be exactly the recorded retained prefix; no
original suffix commit may appear in the rebuilt suffix. If nothing needed
rebuilding in a history-only no-op, the two tips may be identical and no clean
bookmark is required. Extraction can instead end at `REBUILD_BASE` with no
rebuilt suffix and an optional fresh result bookmark. Verify target equality
and every exclusion even though no new clean commit exists; this is not a no-op.
Inspect the full graph:

```sh
jj log -r "$BASE | ($BASE..$ORIGINAL_TIP) | ($BASE..$CLEAN_TIP)"
```

## Failure handling

### A reconstruction operation creates a conflict

Follow [conflict resolution](conflict-resolution.md) for classification,
candidate generation, and correction children. Apply the per-commit protocol
above to every rewritten owner and affected descendant before continuing.

### An original revision was mutated

Stop immediately. Inspect the operation log and patch, then undo only the
offending operation if that is safe in the current repository:

```sh
jj op log
jj op show -p
jj undo
```

The safety tag keeps pointing at the pre-rewrite commit, so use it to prove
exactly what was rewritten. Re-check full original commit IDs before
resuming. If the state cannot be proved, stop and report the uncertainty.

### The wrong revisions were duplicated

Do not incorporate original suffix revisions into the rebuilt suffix.
The explicitly recorded unchanged prefix remains shared and untouched. Abandon only the
newly created duplicates after confirming the exact targets through the
recorded source-to-new mapping, then rebuild from a freshly verified plan.

### Tree equivalence fails

Inspect the full diff and locate dropped, duplicated, mis-split, mis-absorbed,
or conflict-resolved hunks. Repair only duplicate or newly reconstructed
revisions and repeat all validation. Do not declare success with an
unexplained difference.

### An intermediate commit is invalid

Do not hide the dependency. Rebuild the stack from the first affected commit
in a corrected order: move the required foundation earlier in the build,
split the dependent portion, keep inseparable changes together, or merge
them. Re-run checks from the first affected commit onward. For a purely local
repair of content this workflow produced — a split's assembly, a conflict
resolution, a new commit — create a new change on top of the affected
duplicate, fix it there, verify, and squash it into the duplicate per the
operating contract in `SKILL.md`; never edit the duplicate in place. A
finding in preserved original content is a reported caveat, not an unapproved
tree change.

## Report

State the pre-fix and corrected source tips, base, `REBUILD_BASE`, retained prefix and rebuilt
suffix counts, clean tip, the safety tag and clean bookmark with their target
short jj change IDs, original and clean commit counts, fixups folded or
distributed across multiple destinations, preserved semantic milestones,
justified omitted states, splits, reorders, checks run, tree equivalence,
internal original-commit preservation, and remaining caveats. Never expose a
commit ID/Git hash in the report or other user-facing output; identify each
reported revision with at least its short jj change ID and enough role/ref
context to disambiguate it. A result is not complete until every item is
evidenced or explicitly marked unverified.

For extraction, also report retained/excluded features, dependency adaptations,
target tag and identity, full-source-to-target delta audit, and clean-to-target
equality. Distinguish source defects, reconstruction defects, plan/scope errors,
and evidence gaps; the execution report is input to a post-restack review, not
proof that it passed. Such a review reads both histories and actual parent
boundaries, reuses only still-valid evidence, and makes no mutations.

## Definition of done

- When reconstruction occurred, the clean stack is reachable under the new
  clean bookmark.
- The original tip and every original commit ID remain reachable unchanged,
  pinned by the safety tag.
- Existing bookmarks and tags, including the pre-fix and corrected source tags,
  were not moved or deleted.
- The original safety tag still targets the exact original tip. If a clean
  bookmark was created, it targets `CLEAN_TIP`; a clean bookmark is optional
  when no suffix was rebuilt. Extraction to `REBUILD_BASE` still meets the
  target contract.
- Clean and expected-target trees are identical; any difference from the full
  source is exactly the verified authorized fixes/extraction delta. Extraction
  target tags and their preparation evidence remain preserved unchanged.
- Every meaningful incremental state in the original semantic timeline has a
  validated clean destination, including features absent from the final tree;
  every omission has an explicit evidence-backed justification.
- The clean stack has no unexplained conflicts or empty commits.
- No standalone fixup/WIP history remains.
- Commits follow dependency order and have coherent final descriptions in the
  repository's commit-message convention.
- Relevant checks pass at each intermediate commit's own revision; unavailable
  checks block completion. No broken intermediate commits remain.
- Every rebuilt commit's complete parent diff was manually reviewed when the
  commit was created. Every commit whose content or parent tree changed was
  manually reviewed again before rebuilding continued. Description-only
  rewrites have explicit evidence mappings and metadata/graph review. Every
  commit was accounted for in the final oldest-to-newest validation; no rebuilt
  slice was accepted through batch evidence alone.
