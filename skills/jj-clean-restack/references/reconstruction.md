# Reconstruction Tactics

## Analyze intent first

Inspect summaries and diffs for every original commit:

```sh
jj log -r "$OLD_STACK" --summary
jj diff -r "$OLD_STACK" --stat
jj show -r <REVISION>
```

Classify each commit as an independent logical change, exact fixup,
distributed fixup, mixed change, dependency correction, noise, or description
cleanup. Record a destination table before mutating:

| Original | Intent | Destination | Operation |
|---|---|---|---|
| A | foundation | clean 1 | retain |
| B | fixup for A | clean 1 | squash |
| C | mixed implementation/tests | clean 2 and 3 | split |

Prefer dependency order: foundations, core implementation, public integration,
call-site migration, tests, documentation, then independent mechanical work.
The real test is that each commit's parent supplies everything it needs.

## Case coverage

| Situation | Preferred treatment |
|---|---|
| Boundaries already coherent | Duplicate-and-edit; preserve useful commits. |
| Large refactor or repeated rewrites | Final-state rebuild from `OLD_TIP`'s tree. |
| Exact fixup to one owner | Squash into that duplicate/new owner. |
| Hunk spans several owners | Explicitly scoped absorb, then review ambiguous hunks. |
| Mixed behavior and tests | Split so behavior and tests have valid dependencies. |
| Pure mechanical movement | Isolate from behavior when both commits remain checkable. |
| Accidental/noise change | Omit only with approved content change; otherwise preserve it in a coherent commit. |
| Deletion/removal | Treat as a first-class change; use `jj revert` for a known duplicate change, then add any replacement later. |
| Generated artifact | Follow repository policy; never silently drop it while claiming tree equivalence. |
| Conflict or invalid intermediate | Stop, rebuild the duplicate/new stack from the first affected commit, and re-check. |

## Select a reconstruction mode

Apply either mode only to the suffix after `REBUILD_BASE`, keeping the
longest unchanged prefix intact as defined in `scope-and-safety.md`.

### Duplicate-and-edit mode

Use this only when most original boundaries already represent useful logical
changes and the main work is folding fixups, correcting order, or improving
descriptions. Decide the final order and treatment of every commit first,
then build the clean stack by duplicating one source revision at a time onto
the current clean tip (see "Build the clean stack one commit at a time" in
`scope-and-safety.md`). Never duplicate the whole range at once and reorder
afterwards, and never use `jj rebase` to place revisions: the order is
realized by the build itself. Apply the tactics below to the duplicate
revisions as the build reaches them, and inspect after every step.

### Final-state rebuild mode

Use this for large refactors, repeated rewrites of the same files, commits
whose diffs cannot be assigned reliably, or a stack where subjects and
boundaries no longer describe the final design. The final tree is the source
of truth; commit provenance is not.

1. Preserve the original tip and commit-ID list as usual.
2. Create a new child of `REBUILD_BASE`; retain the original prefix and do
   not import any original suffix commits.
3. Restore the old tip's final tree into that new revision:

   ```sh
   jj restore --from "$OLD_TIP" --into <NEW_REVISION>
   ```

   Check `jj help restore` if the installed version differs, and record the
   source and destination revisions.
4. Partition only the net suffix change relative to `REBUILD_BASE` into planned logical commits using `jj split`,
   interactive editing, or small explicit edits. Give each commit a complete
   purpose and description.
5. If a final-state change must be removed or corrected, make the subtraction
   explicit before adding the replacement. Validate the resulting final tree
   against the original unless the user approved a content change.

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

All placeholders below must resolve to duplicate revisions.

### Exact fixup to one owner

```sh
jj squash --from <FIXUP> --into <OWNER> --use-destination-message
```

Use a path or `--interactive` when only part of the source belongs there.
Inspect the owner and nearby history afterward. Remove an emptied duplicate
only when it is genuinely redundant; never remove an original revision.

### Distributed fixup

Use `jj absorb` only with an explicit destination revset restricted to the
duplicate stack and intended ancestors. Do not rely on its default mutable
scope. Review the resulting operation (for example with `jj op show -p`) and
manually handle ambiguous hunks with interactive squash or split.

### Mixed commit

Split the duplicate revision and give every resulting commit a coherent
description:

```sh
jj split -r <DUPLICATE_REVISION>
```

Use path selection when concerns divide by files. Use insertion options only
after verifying the installed `jj split` syntax and the extracted change's
dependencies.

### Reordering

Order is chosen during analysis and realized by the build: duplicate the
next source revision onto the current clean tip in the final order. A
revision that must come earlier is simply built earlier. Do not duplicate
the whole range first and move duplicate revisions afterwards.

If a build step exposes a real dependency — the duplicate conflicts, or its
tree is missing something its source had — stop building and adjust the
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

Describe only duplicate revisions. State what the commit accomplishes and why
when non-obvious. Do not mention `fixup`, `wip`, review cleanup, or the
restacking process. The final history should read as intentional history.

Format every description in the repository's commit-message convention —
check recent subjects with `jj log` to detect it (for example Conventional
Commits). Use a concise imperative subject line of at most about 72
characters, and a body only when the reasoning is not obvious. Never leave a
placeholder or auto-generated description on a clean commit.

## Command guide

| Goal | Command family |
|---|---|
| Build the clean stack | `jj duplicate --onto`, one source revision at a time |
| Fold one fixup | `jj squash` |
| Distribute a fixup | `jj absorb` with explicit `--into` |
| Separate concerns | `jj split` |
| Place a revision at a new position | `jj duplicate --onto` during the build (never `jj rebase`) |
| Review the latest operation | `jj op show -p` |
