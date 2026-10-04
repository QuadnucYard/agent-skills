# Scope And Safety

## Freeze the original

Use explicit revision expressions, preferably full commit IDs. Naming an
existing ref the user points at is fine, but this skill itself never creates
or moves a bookmark:

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

Tags are used instead of bookmarks because jj moves a bookmark automatically
when its commit is rewritten, while a tag stays on the exact commit — if
anything ever rewrites the original stack, the tag still points at the
untouched original. If the proposed name exists, use another name; never
move or delete a tag (`--allow-move` is not part of this workflow).

## Preserve first; build selectively

The original range must always be preserved before reconstruction, but
duplication is incremental. Use duplicate-and-edit only when inspection shows
that commit boundaries are mostly coherent, and build that clean stack one
commit at a time as described below. For a tangled refactor or history whose
intermediate states are not useful, use the final-state rebuild mode in
`reconstruction.md` and create new revisions from `REBUILD_BASE` instead.

After analyzing the complete range, retain its longest initial prefix whose
content, descriptions, and order already fit the final plan. Record its full
commit IDs and set `REBUILD_BASE` to its tip, or `BASE` if no prefix qualifies.
A later fixup targeting a prefix commit makes that commit part of the suffix
to rebuild. Reuse only this contiguous prefix, never scattered original
commits after divergence. If all commits qualify, no reconstruction is needed.
The original range remains `OLD_STACK`; only new suffix commits belong to
`NEW_STACK`, while `BASE..CLEAN_TIP` denotes the complete clean stack.

## Build the clean stack one commit at a time (when boundaries are reusable)

Do not duplicate the whole range up front. Decide the final order and each
commit's treatment during analysis (see `reconstruction.md`), then build the
clean stack incrementally so every revision lands exactly where it belongs.

Start with `CURRENT_TIP=$REBUILD_BASE`. For each remaining source revision
in the final order (skip the retained prefix):

```sh
jj duplicate "$NEXT_SOURCE" --onto "$CURRENT_TIP"
```

Set `CURRENT_TIP` to the new duplicate's change ID from the command output,
record the source-to-new mapping, and verify the step before continuing.
Do not infer the new tip from `@`, timestamps, or descriptions.

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
place (see the operating contract in `SKILL.md`).

Fold a fixup as part of the build: duplicate it immediately after its owner,
squash it into the owner duplicate, and continue building; the temporary
fixup duplicate does not survive. Because each source revision is duplicated
individually, a commit the user approved to omit is simply left out of the
build instead of being removed afterwards.

When the build is complete, record the clean tip's full commit ID, pin it
with the clean tag, and define the duplicate range:

```sh
CLEAN_TIP=$(jj log -r "$CURRENT_TIP" --no-graph -T 'commit_id')
jj tag set "$CLEAN_TAG" -r "$CURRENT_TIP"
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
`restore`, `split`, or `squash`:

1. Resolve source and destination revisions explicitly. For `duplicate`, the
   destination must be `REBUILD_BASE` or the current clean tip. Reading or
   using a retained original as a parent is allowed; rewriting it is not.
2. Confirm every rewritten revision is in `NEW_STACK`.
3. Confirm no target intersects `OLD_STACK` or `BASE`.
4. Prefer a narrow revision/path selection over `mutable()`, `all()`, or
   `mine()`.

Useful checks:

```sh
jj log -r "(<TARGET_REVSET>) & ($NEW_STACK)" \
  -T 'commit_id.short() ++ " " ++ description.first_line() ++ "\\n"'
jj log -r "(<TARGET_REVSET>) & ($OLD_STACK)"
```

The first should show every intended target; the second must be empty. If a
command refuses to rewrite a revision, stop and investigate. Do not bypass
immutability protection.

## Tag and publication rules

Never repoint, move, or delete a pre-existing bookmark or tag, and never
move the safety or clean tags. Never force-push the clean stack over the
original. Publishing, if requested, is a separate explicit operation after
validation.
