# Validation And Recovery

## Required validation

The clean tip must equal the verified source target. `ORIGINAL_TIP` is the
corrected source tip when planned fixes were committed, otherwise the pre-fix
source tip. For both cases:

```sh
jj diff --from "$ORIGINAL_TIP" --to "$CLEAN_TIP" --summary
jj diff --from "$ORIGINAL_TIP" --to "$CLEAN_TIP" --git
```

With fixes, also inspect the pre-fix-to-corrected and pre-fix-to-clean diffs:
both must contain exactly the planned, authorized changes. Never claim equality
to the pre-fix tree when those trees differ.

Tip equivalence is necessary but insufficient. Compare the rebuilt sequence to
the semantic timeline recorded during analysis. Every meaningful incremental
feature, migration or compatibility stage, deprecation, and intentional
removal must appear at an appropriate clean commit, including states no longer
present in `OLD_TIP`. For every omitted original state, verify the recorded
finding that it was fixup noise, invalid partial work, or otherwise not an
intended reviewable milestone.

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
build/test/type/lint checks. Do not claim intermediate validity if a check was
not run or cannot be run.

This final pass confirms, but does not replace, the manual gate performed
immediately after each rebuilt commit was created. Every rebuilt slice must
have a recorded commit-by-commit review. There is no valid batch review of a
slice. If a later squash, absorb, split, conflict resolution, or description
rewrite changes an already reviewed commit, its prior validation is stale;
repeat the full protocol for every rewritten commit and affected descendant
before continuing the rebuild.

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
   relevant integration tests, build/type checks, lints, and formatting checks.
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
shows `CLEAN_BOOKMARK` on `CLEAN_TIP`. Inspect the final graph and confirm the
clean stack is a separate suffix rooted at `REBUILD_BASE`. Its intersection
with the original range must be exactly the recorded retained prefix; no
original suffix commit may appear in the rebuilt suffix. If nothing needed
rebuilding, the two tips may be identical and no clean bookmark is required.
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

## Definition of done

- When reconstruction occurred, the clean stack is reachable under the new
  clean bookmark.
- The original tip and every original commit ID remain reachable unchanged,
  pinned by the safety tag.
- Existing bookmarks and tags, including the pre-fix and corrected source tags,
  were not moved or deleted.
- The original safety tag still targets the exact original tip, and the clean
  bookmark targets the rebuilt tip.
- Clean and original tip trees are identical.
- Every meaningful incremental state in the original semantic timeline has a
  validated clean destination, including features absent from the final tree;
  every omission has an explicit evidence-backed justification.
- The clean stack has no unexplained conflicts or empty commits.
- No standalone fixup/WIP history remains.
- Commits follow dependency order and have coherent final descriptions in the
  repository's commit-message convention.
- Rebuild-produced content passes the repository's formatter and linters;
  formatting findings in preserved original content are reported as caveats,
  not fixed silently.
- Relevant checks pass at each intermediate commit's own revision; unavailable
  checks block completion. No broken intermediate commits remain.
- Every rebuilt commit's complete parent diff was manually reviewed when the
  commit was created. Every commit rewritten by a later multi-destination
  absorb, squash, split, or descendant rebase was manually reviewed again
  before rebuilding continued, and every commit was accounted for in the final
  oldest-to-newest validation; no rebuilt slice was accepted through batch
  evidence alone.
