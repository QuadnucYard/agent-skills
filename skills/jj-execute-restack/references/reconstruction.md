# Reconstruction Tactics

Execute the supplied inventory, semantic timeline, and redistribution map.
Choose mechanics within those boundaries; return changed purposes, dependencies,
or uncertain ownership to planning. Read the scope-and-safety mutation gate
before each operation.

## Case coverage

| Situation | Preferred treatment |
| --- | --- |
| A small minority of commits have coherent, mostly reusable boundaries | Duplicate only that confirmed slice, one explicit revision at a time. |
| Large refactor or repeated rewrites | Reconstruct from identified semantic milestones; use final-state partitioning only if no meaningful intermediate state would be lost. |
| Exact fixup whose complete diff belongs to one owner | Squash into that duplicate/new owner. |
| Later commit contains hunks for several owners | Map hunks to all destinations, then use explicitly scoped absorb or split. |
| One feature spanning implementation, integration, and tests | Keep together as a coherent vertical slice. |
| Several features mixed across crates or layers | Split by semantic feature, including each feature's integration and tests. |
| Selected features excluded from the result | Reconstruct the dependency-closed retained set; compare to the separately pinned extraction target, accounting for all excluded hunks and shared support. |
| Pure mechanical movement | Isolate from behavior when both commits remain checkable. |
| Accidental/noise change | Omit only with approved content change; otherwise preserve it in a coherent commit. |
| Deletion/removal | Treat as a first-class change; use `jj revert` for a known duplicate change, then add any replacement later. |
| Generated artifact | Follow repository policy; never silently drop it while claiming tree equivalence. |
| Explained structural conflict | Resolve in a correction child using the conflict-resolution reference, then revalidate the owner and affected descendants. |
| Missing dependency or invalid intermediate | Stop, revise the build plan from the first affected commit, and re-check. |

## Select reconstruction tactics

Apply these tactics only to the suffix after `REBUILD_BASE`, keeping the
longest unchanged prefix intact as defined in `scope-and-safety.md`. Choose the
source for each clean commit from its intended semantic milestone; do not
choose one reconstruction mode for the whole suffix by convenience.
Duplication is only a local optimization for a small confirmed slice and must
never become a second copy of the original stack.

### State equality versus change reuse

`jj restore` replaces selected content with a source state, rather than applying
a change. Use it only for intended state equality and inspect overwritten fixes
and hunk ownership. For example, restoring a later snapshot can hide a missed
comment update by introducing it in the wrong commit; fix its actual owner.
To pick all or most of one change, use `jj duplicate` within the confirmed-slice
limits below. Reconstruct substantially redistributed changes from diffs and edits.

### History-aware selective reconstruction

This is the general tactic when original commits need substantial cleanup but
their sequence contains meaningful states. Build each planned clean commit
from the relevant original parent-to-commit diffs, milestone tree, and explicit
edits. A clean commit may combine hunks from several original commits or
represent an incremental state later absent from `OLD_TIP`. Materialize exactly
one planned milestone, manually validate its complete parent diff and behavior,
advance `CLEAN_BOOKMARK`, then continue.

Do not require a one-to-one mapping between original and clean commits. Do
require every meaningful original milestone to have a named clean destination
or a recorded justification for omission. If a milestone was later removed,
the clean history may need both the feature-introduction commit and a later
intentional-removal commit even though their net effect is absent at the tip.

### Confirmed-slice duplication

Use this only when a small minority of the original commits already represent
useful logical changes and all or most of each selected commit will survive
unchanged. Manually inspect every selected source commit under the evidence
requirements in `scope-and-safety.md` before duplicating any of them. Name the
bounded slice explicitly, then duplicate one source revision at a time onto
the current clean tip. Never pass a range to `jj duplicate`, duplicate the
whole original stack or changed suffix, or assemble multiple duplicate slices
that collectively do so. Never use `jj rebase` to place revisions. After each
resulting clean commit, read its full parent diff and validate its intent,
dependencies, and relevant behavior before proceeding.

### Qualified final-state reconstruction

Use this only when a commit-by-commit semantic audit proves that the original
suffix contains no meaningful intermediate feature, migration, compatibility
stage, or intentional removal that would be hidden by `OLD_TIP`. Typical
qualifying content is repeated fixup noise or invalid partial work whose only
intended state is the final result. The final tree is then a reconstruction
source, not proof that this tactic is safe.

1. Preserve the original tip and commit-ID list as usual.
2. Record the semantic audit and the justification for omitting every original
   intermediate state from the clean sequence. If any state lacks a confident
   disposition, use history-aware selective reconstruction instead.
3. Create a new child of `REBUILD_BASE`; retain the original prefix and do
   not import any original suffix commits.
4. Restore the expected target's final tree into that new revision for state equality,
   checking for overwritten fixes as described above:

   ```sh
   jj restore --from "$EXPECTED_TIP" --into <NEW_REVISION>
   ```

   Check `jj help restore` if the installed version differs, and record the
   source and destination revisions.
5. Partition only the net suffix change relative to `REBUILD_BASE` into planned
   logical commits using `jj split`, interactive editing, or small explicit
   edits. Materialize one planned commit, give it a complete purpose and
   description, and validate it before extracting the next. Do not create a
   batch of unchecked commits.
6. After producing each commit, manually read its complete diff against its
   actual clean parent, confirm its single stated purpose and dependency
   completeness, and run the relevant behavioral check before splitting or
   creating the next commit.
7. If a final-state change must be removed or corrected, make the subtraction
   explicit before adding the replacement. Validate the resulting final tree
   against `EXPECTED_TIP`. In extraction, never restore the full old tip as a
   residual: that would reintroduce excluded features. The semantic audit must
   still account for each excluded intermediate state explicitly.

### Mixed-source sequencing

When clean history combines selectively reconstructed milestones, confirmed
duplicate slices, and possibly a qualified final-state partition, apply each
source only at its planned semantic position. Do not restore the full final
tree and then duplicate or reconstruct content already present; that would
apply it twice. Build and validate each planned commit before selecting the
source for the next. The combined duplicated revisions must remain a small
minority and must never collectively reproduce the original stack or changed
suffix.

At every boundary, inspect the complete diff of the next planned commit, its
source milestone, and the current-tip-to-`EXPECTED_TIP` diff. Confirm that no hunk
already introduced is applied again, no required final hunk is lost, and no
required intermediate state is skipped. If that accounting is uncertain, stop
and revise the milestone and destination maps; do not collapse to a final-state
rebuild as a shortcut.

Do not use duplication merely because it is mechanically convenient. A clean
stack with correct final content and independently valid commits is preferable
to preserving misleading intermediate provenance.

## Add versus subtract

For every planned commit, state whether it adds, modifies, or removes behavior
relative to its parent. Keep the net delta small and attributable.

- **Add:** introduce a new file, API, behavior, test, or migration, then check
  it at that commit.
- **Modify/refactor:** keep mechanical movement separate from behavior changes
  when that makes review and checks meaningful.
- **Subtract:** remove an unwanted change explicitly. When the unwanted change
  corresponds to an existing duplicate commit, prefer `jj revert` on the
  duplicate/new stack so the inverse is recorded as an intentional change.
  Use the installed version's `jj revert` help to confirm revision and path
  syntax; never revert an original revision in place.

Example shape (placeholders are deliberately explicit):

```sh
jj revert --revision <DUPLICATE_CHANGE_TO_REMOVE> \
  --onto <DUPLICATE_OR_NEW_TARGET>
```

If only selected paths or hunks should be removed, use the version-supported
path/interactive form, or create a new change on top of the duplicate, make
the subtraction there, verify it, and squash it into the duplicate per the
operating contract in `SKILL.md`. Do not use `revert`
to conceal a dependency problem or to make an original stack appear clean.
After subtracting, add the intended replacement in a later coherent commit.
The inverse and replacement should each pass their own checks.

## Choose the narrowest operation

All placeholders below must resolve to revisions in the rebuilt suffix, never
the original stack.

### Exact fixup to one owner

```sh
jj squash --from <FIXUP> --into <OWNER> --use-destination-message
```

Use squash only after manually confirming that the complete source diff belongs
to this single owner. If only part belongs there, do not simplify the source to
one destination: use a path or `--interactive` for that part and explicitly
route the remainder to its other owners. Inspect and manually revalidate the
owner and every rewritten descendant afterward. Remove an emptied duplicate
only when every hunk has reached its correct destination and it is genuinely
redundant; never remove an original revision.

### Distributed fixup

A later commit can be a fixup for multiple earlier rebuilt commits. Do not
choose one owner for convenience. Read its complete diff, assign every hunk to
one or more intended logical destinations, and record that map before mutation.
Use `jj absorb` only with an explicit destination revset containing all and
only those rebuilt destinations. Do not rely on its default mutable scope.
Review the resulting operation (for example with `jj op show -p`) and manually
handle ambiguous hunks with interactive squash or split.

Line provenance is not semantic ownership, especially across moved or extracted
code. When it disagrees with the destination map, reconstruct corrections in
their intended owners' earlier structures or split explicitly. Resolve any
structural conflicts in rewritten descendants with
[conflict resolution](conflict-resolution.md), not by editing destinations.

Absorption rewrites its destinations and may rewrite descendants. Immediately
inspect and manually validate each rewritten destination from oldest to newest,
then each affected rebuilt descendant against its new parent. Do not create,
absorb, or split the next source commit until all of those validations pass.
Re-resolve `CURRENT_TIP` and verify that `CLEAN_BOOKMARK` points to it after
the rewrite.

### Mixed commit

Split the duplicate revision and give every resulting commit a coherent
description:

```sh
jj split -r <DUPLICATE_REVISION>
```

Use path selection when concerns divide by files. Use insertion options only
after verifying the installed `jj split` syntax and the extracted change's
dependencies. Treat every result as newly rebuilt: manually validate each
resulting commit from oldest to newest before any further split or mutation.

### Reordering

Order is chosen during semantic-timeline analysis and realized while building
one milestone at a time. When a confirmed small slice is reused, duplicate its
next explicit source revision onto the current clean tip in the final order. A
revision that must come earlier is built earlier. Do not duplicate the whole
range first or move finished revisions afterwards.

An explained mechanical overlap can follow
[conflict resolution](conflict-resolution.md). If a build step exposes a real
dependency or its tree is missing something its source had, stop and adjust the
plan: move the foundation earlier in the build order, keep dependent changes
together, or merge them when they are not independently coherent. Do not
leave a broken intermediate commit.

After every build step:

```sh
jj log -r "$BASE | ($BASE..$CURRENT_TIP)"
jj log -r "conflicts() & ($BASE..$CURRENT_TIP)"
```

Reordering is justified by semantic/build dependencies, not cosmetic subject
order.

## Descriptions

Describe only duplicate or newly reconstructed revisions. State what the
commit accomplishes and why when non-obvious. Do not mention `fixup`, `wip`,
review cleanup, or the restacking process. The final history should read as
intentional history.

Format every description in the repository's commit-message convention —
check recent subjects with `jj log` to detect it (for example Conventional
Commits). Use a concise imperative subject line of at most about 72
characters, and a body only when the reasoning is not obvious. Never leave a
placeholder or auto-generated description on a clean commit.

## Command guide

| Goal | Command family |
| --- | --- |
| Reconstruct a semantic milestone | selected original diffs, `jj split`, or explicit edits from original evidence |
| Make selected content equal a source state | scoped `jj restore`, after checking overwritten fixes and hunk ownership/timing |
| Partition a qualified final state | `jj restore` plus `jj split`, only after the semantic audit |
| Reuse a confirmed small slice | `jj duplicate --onto`, one explicit source revision at a time |
| Fold a wholly single-owner fixup | `jj squash` |
| Distribute a multi-owner fixup | `jj absorb` with explicit `--into`, or split by hunk |
| Separate concerns | `jj split` |
| Place a confirmed reusable revision | `jj duplicate --onto` within the small approved slice (never `jj rebase`) |
| Review the latest operation | `jj op show -p` |
