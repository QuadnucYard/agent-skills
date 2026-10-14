# Scope And Safety

## Freeze the original

Use explicit revision expressions, preferably full commit IDs. Naming an
existing ref the user points at is fine. The only bookmark this workflow may
create or move is the new dedicated `CLEAN_BOOKMARK`:

```sh
BASE=<parent-or-base>
OLD_TIP=<messy-tip>
OLD_STACK="$BASE..$OLD_TIP"
```

Inspect the graph and tree:

```sh
jj log -r "$BASE | $OLD_STACK" --summary
jj log -r "$OLD_STACK" --no-graph
jj diff --from "$BASE" --to "$OLD_TIP" --stat
jj log -r "merges() & ($OLD_STACK)"
```

Require exactly one `BASE` and one `OLD_TIP`, the intended range, and no
unexpected merges. If the stack is not linear, stop unless the user has
specified how merge structure should be retained.

Record full commit IDs, not only change IDs:

```sh
jj log -r "$OLD_STACK" --no-graph -T 'commit_id ++ "\\n"'
```

Change IDs are insufficient because rewritten versions can retain a change ID.
Use a file outside the repository when possible, with a path appropriate to
the host rather than assuming `/tmp` exists.

Pin the original tip with a new tag, and keep its full commit ID in a
variable for revset use:

```sh
jj tag set "$ORIGINAL_TAG" -r "$OLD_TIP"
ORIGINAL_TIP=$(jj log -r "$OLD_TIP" --no-graph -T 'commit_id')
```

Use a tag, not a bookmark, for original-stack safety because jj moves a
bookmark automatically when its commit is rewritten, while a tag stays on the
exact commit. If anything ever rewrites the original stack, the tag still
points at the untouched original. If the proposed name exists, use another
name; never move or delete a tag (`--allow-move` is not part of this workflow).

Reserve a new, unused `CLEAN_BOOKMARK` name for the rebuilt stack. Create it
after the first rebuilt commit passes its immediate manual validation, point it
at `CURRENT_TIP`, and advance it only after each new tip passes the same gate:

```sh
jj bookmark create "$CLEAN_BOOKMARK" -r "$CURRENT_TIP"
jj bookmark set "$CLEAN_BOOKMARK" -r "$CURRENT_TIP"
```

The first command is used once; subsequent advances use the second. Confirm
the installed jj syntax before mutation. The bookmark may follow rewritten
commits automatically, but always verify its exact target rather than relying
on that behavior.

## Preserve first; reconstruct selectively

The original range must always be preserved before reconstruction. Do not
duplicate it as a convenient starting point. Rebuild the changed suffix from a
recorded semantic timeline of the original commits, using their individual
diffs and milestone trees as evidence. Do not assume `OLD_TIP` alone represents
the history: later commits may obscure or remove incremental features that must
remain reviewable. Use duplication only to reuse a small, explicitly named
slice after every source commit in that slice has been manually inspected and
confirmed as fully or mostly suitable for the clean history. Duplication must
not collectively reproduce the original stack, even through several separate
commands or slices.

After analyzing the complete range, retain its longest initial prefix whose
content, descriptions, and order already fit the final plan. Record its full
commit IDs and set `REBUILD_BASE` to its tip, or `BASE` if no prefix qualifies.
A later fixup targeting a prefix commit makes that commit part of the suffix
to rebuild. Reuse only this contiguous prefix, never scattered original
commits after divergence. If all commits qualify, no reconstruction is needed.
The original range remains `OLD_STACK`; only new suffix commits belong to
`NEW_STACK`, while `BASE..CLEAN_TIP` denotes the complete clean stack.

## Reuse a small confirmed slice (exception only)

Do not duplicate the whole range, the whole changed suffix, or a series of
slices that has the same effect. A proposed slice must be a short, bounded
list of explicit revisions and small relative to the original stack. Before
any duplication, manually read the complete diff of every source commit and
record:

1. the logical purpose and dependencies of the commit;
2. why its boundary is already useful in the planned clean history;
3. which content will be retained unchanged and why that is all or most of
   the commit; and
4. every edit, split, squash, or description change still required.

If any commit is unclear, substantially rewritten, or useful only as raw
material for several destinations, exclude it from the slice and reconstruct
that content from its source diffs, relevant milestone trees, and explicit
edits. If the confirmed revisions are not a small minority of the original
stack, abandon duplication and use history-aware selective reconstruction.

Start with the current clean tip. For each source revision in the confirmed
slice, in the planned final order:

```sh
jj duplicate "$NEXT_SOURCE" --onto "$CURRENT_TIP"
```

Set `CURRENT_TIP` to the new duplicate's change ID from the command output,
record the source-to-new mapping, and manually validate the resulting commit
before continuing. Read its complete diff against its actual clean parent;
confirm that the diff has one coherent purpose, contains no accidental or
missing hunks, and has all required dependencies; then run the relevant
behavioral check. A summary or automated check alone is insufficient.
Advance `CLEAN_BOOKMARK` to the verified `CURRENT_TIP`. Do not infer the new
tip from `@`, timestamps, descriptions, or the bookmark itself.

```sh
jj log -r "$CURRENT_TIP" --no-graph \
  -T 'commit_id.short() ++ " " ++ description.first_line() ++ "\\n"'
jj diff -r "$CURRENT_TIP" --stat
```

When the step preserves the original order, the duplicate's tree must match
its source's:

```sh
jj diff --from "$NEXT_SOURCE" --to "$CURRENT_TIP" --summary
```

That must be empty; if it is not, stop — the wrong source, base, or
destination was used. When the step places a revision at a new position,
confirm the planned dependency is present. Resolve any conflict in a new
change created on top of the new duplicate, verify the resolution, then
squash it into the duplicate; never resolve by editing the duplicate in
place (see [conflict resolution](conflict-resolution.md)).

When a fixup is part of a confirmed small slice, first inspect it hunk by hunk.
Squash it only if its complete diff belongs to one owner. If it changes several
earlier logical commits, use an explicitly bounded absorb destination set or
split it among those destinations. Manually revalidate every rewritten owner
and affected descendant before continuing; the temporary fixup duplicate does
not survive. Outside such a slice, reconstruct each fixup hunk directly in its
planned destination or destinations.

When the build is complete, record the clean tip's full commit ID, point the
clean bookmark at it, and define the rebuilt suffix:

```sh
CLEAN_TIP=$(jj log -r "$CURRENT_TIP" --no-graph -T 'commit_id')
jj bookmark set "$CLEAN_BOOKMARK" -r "$CLEAN_TIP"
NEW_STACK="$REBUILD_BASE..$CLEAN_TIP"
```

Regardless of order, the clean tip's tree must match the original tip's tree
before cleanup continues (unless the user approved a content change):

```sh
jj diff --from "$ORIGINAL_TIP" --to "$CLEAN_TIP" --summary
```

If the result is non-empty, stop. The wrong range, base, order, or mapping
was used.

## Mutation gate

Before every `jj abandon`, `absorb`, `describe`, `diffedit`, `duplicate`,
`new`, `resolve`, `restore`, `split`, or `squash`:

1. Resolve source and destination revisions explicitly. For `duplicate`, the
   destination must be `REBUILD_BASE` or the current clean tip. Reading or
   using a retained original as a parent is allowed; rewriting it is not.
2. Confirm every rewritten revision is in `NEW_STACK` or is an explicitly
   recorded temporary correction child owned by this reconstruction. A
   correction branch need not be an ancestor of the current clean tip.
3. Confirm no rewritten target intersects `OLD_STACK` or `BASE`. A parent
   used by `new` is read-only and may be `REBUILD_BASE`.
4. Prefer a narrow revision/path selection over `mutable()`, `all()`, or
   `mine()`.
5. For `resolve`, the target must be the temporary correction child, never
   a completed rebuilt commit. For `new`, verify its parent and preserve
   unrelated working-copy changes; do not insert it into original history.
6. For `restore`, confirm the intended state equality and inspect overwritten
   fixes and hunk ownership/timing as described in the reconstruction reference.

Useful checks (`CORRECTION_REVSET` is the explicitly recorded correction-child
set, or `none()` when no correction exists):

```sh
jj log -r "(<TARGET_REVSET>) & ($NEW_STACK | ($CORRECTION_REVSET))" \
  -T 'commit_id.short() ++ " " ++ description.first_line() ++ "\\n"'
jj log -r "(<TARGET_REVSET>) & ($OLD_STACK)"
```

The first should show every intended target; the second must be empty. If a
command refuses to rewrite a revision, stop and investigate. Do not bypass
immutability protection.

## Reference and publication rules

Never repoint, move, or delete a pre-existing bookmark or tag, and never
move the safety tag. The only movable reference is the newly created
`CLEAN_BOOKMARK`, which must point to the current rebuilt tip. Never force-push
the clean stack over the original. Publishing, if requested, is a separate
explicit operation after validation.
