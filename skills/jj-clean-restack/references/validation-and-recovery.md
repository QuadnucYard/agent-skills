# Validation And Recovery

## Required validation

The clean and original tips must have identical trees unless the user
explicitly approved a content change. For the normal case:

```sh
jj diff --from "$ORIGINAL_TIP" --to "$CLEAN_TIP" --summary
jj diff --from "$ORIGINAL_TIP" --to "$CLEAN_TIP" --git
```

For an approved content change, compare the clean tip to the explicitly
approved target and report the intentional delta; do not call it equivalent to
the original tree.

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

## Per-commit check protocol

For each clean commit, from oldest to newest:

1. Inspect the commit and its parent diff. Confirm every referenced symbol,
   schema, generated file, and test fixture is provided by the parent or the
   commit itself.
2. Check the commit at that revision in an isolated working state (for example
   with the repository's established `jj edit`/`jj new` workflow). The tags
   pin both tips, so checking out an intermediate commit cannot lose either
   endpoint.
3. Run checks proportional to the change: focused unit tests first, then the
   relevant integration tests, build/type checks, lints, and formatting checks.
   A refactor must run behavior/regression tests, not only compilation.
4. Record the exact commands and outcomes. A failed or skipped check is a
   blocking caveat, not a passing commit.

At minimum, the oldest rebuilt commit must build against `REBUILD_BASE`; every
later commit must build against its immediate clean parent. Inspect the retained
prefix for unchanged IDs and coherent behavior, and report relevant existing
validation evidence or gaps. If a commit cannot be
validated independently, split it differently or keep it with the dependency
it requires.

Verify the original commit-ID list is unchanged, and that `jj tag list`
still shows `ORIGINAL_TAG` on the recorded original tip and `CLEAN_TAG` on
the clean tip. Inspect the final graph and confirm the clean stack is a
separate suffix rooted at `REBUILD_BASE`. Its intersection with the original
range must be exactly the recorded retained prefix; no original suffix
commit may appear in the rebuilt suffix. If nothing needed rebuilding,
the two tips may be identical. Inspect the full graph:

```sh
jj log -r "$BASE | ($BASE..$ORIGINAL_TIP) | ($BASE..$CLEAN_TIP)"
```

## Failure handling

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
or conflict-resolved hunks. Repair only duplicate revisions and repeat all
validation. Do not declare success with an unexplained difference.

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

State the original base/tip, `REBUILD_BASE`, retained prefix and rebuilt
suffix counts, clean tip, both tags and the commit IDs they
pin, original and clean commit counts, fixups folded/distributed, splits,
reorders, checks run, tree equivalence, original-ID preservation, and
remaining caveats. A result is not complete until every item is evidenced or
explicitly marked unverified.

## Definition of done

- The clean stack is reachable under the new clean tag.
- The original tip and every original commit ID remain reachable unchanged,
  pinned by the safety tag.
- Existing bookmarks and tags were not moved or deleted.
- Clean and original tip trees are identical.
- The clean stack has no unexplained conflicts or empty commits.
- No standalone fixup/WIP history remains.
- Commits follow dependency order and have coherent final descriptions in the
  repository's commit-message convention.
- Rebuild-produced content passes the repository's formatter and linters;
  formatting findings in preserved original content are reported as caveats,
  not fixed silently.
- Relevant checks were run for each intermediate commit, or limitations are
  reported.
