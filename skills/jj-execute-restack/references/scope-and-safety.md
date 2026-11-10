# Scope And Safety

## Behavior-preserving mainline

If the plan requires behavior preservation, its explicit baseline governs the
mainline. Route every behavior-changing feature or fix to residuals; source
membership or separate fix authorization does not override this constraint.
Do not include residual fixes in the corrected mainline target. Use the
extraction-target phase when the source includes residual behavior, and verify
the retained result against the baseline contract as well as the target tree.

For residuals requested for reference, build separate workflow-owned branches
from their planned dependency-appropriate milestones, each with a fresh bookmark.
Record their revisions separately from `NEW_STACK` and correction children;
they must not be mainline ancestors. Apply the mutation gate and per-commit
validation to each residual branch. Pure reconstruction repairs restore the
planned baseline; new source defects remain residual recommendations unless
their implementation is authorized on a side branch.

## Planned source fixes

Verify the plan's exact source snapshot, relevant refs, and unrelated working-copy
state before mutation. Record the operation and pre-fix source identities. Pin
`SOURCE_TIP` with a fresh `SOURCE_TAG` before any fix. Tags never move.

Only planned, authorized fixes may extend this source: create explicit children
of the recorded source tip, keep unrelated edits separate, and review and test
each fix before continuing. Original commits remain unchanged; do not insert,
squash, or absorb fixes into them. Record each verified fix and its clean owner.
This source-fix phase permits new top commits, not reconstruction rewrites.

After fixes, pin their final verified tip with a fresh `ORIGINAL_TAG` and use it
as `OLD_TIP` below. Without fixes, `ORIGINAL_TAG` is the existing `SOURCE_TAG`.
Verify the pre-fix-to-corrected delta against the plan. All later reconstruction
mutations follow the gate below. If a new source fix is required, return to
planning and repeat the source-fix phase with fresh target records and tags.

## Prepare an extraction target

This preparation applies on the same base. For another base, compose extraction
into the integration target in [destination preparation](#another-destination-base).

Same-base restacks without extraction set `EXPECTED_TIP=OLD_TIP`. When the plan explicitly excludes
features, `OLD_TIP` remains the corrected full source; prepare a separate target
before reconstructing. Require a complete retained/excluded feature map,
source-hunk ownership, dependency closure, authorized adaptations, and expected
source-to-target delta. Missing dependency decisions block affected work.

Create explicit new children of `OLD_TIP` on a separate target-preparation line.
Apply only planned feature subtractions and adaptations; never rewrite source
commits or derive this target by copying the rebuilt tip. This phase permits
new top commits, as the source-fix phase does, not edits of completed revisions.
Record each target-preparation commit separately from fixes and clean owners.
Preserve support required by retained consumers and remove excluded-only wiring,
APIs, configuration, tests, documentation, and generated/dependency artifacts.
Do not erase base behavior or migrations outside the authorized scope.

Read the complete `OLD_TIP`-to-target diff against the planned exclusion map,
including hunks in shared files. Check retained production paths, compatibility,
and absence of excluded entry points; run the relevant behavior/build checks.
Pin the verified result with a fresh immutable `TARGET_TAG`, record its exact
commit/tree identities as `EXPECTED_TIP`, and retain the target-preparation
evidence. The rebuilt stack must match this target, but must not inherit these
subtraction commits as a shortcut to clean history.

With fixes, separately validate pre-fix-to-`OLD_TIP` as fixes and
`OLD_TIP`-to-`EXPECTED_TIP` as extraction; inspect the combined delta too, since
overlapping changes can mask mistakes. A changed selection or adaptation returns
to planning and gets a fresh target/tag; never move an old tag or accept an
unexpected rebuilt delta as the new specification.

## Another destination base

Keep `BASE` and `OLD_STACK` tied to the source. Verify and protect the exact
`DESTINATION_BASE` commit/tree from the plan and set `REBUILD_BASE` to it,
rather than defaulting to `BASE` or an unrelated source-prefix tip. Normally
there is no reusable source prefix; original commits already in destination
ancestry are base-provided history, not replay candidates. Never rewrite the
destination or move its existing refs. Destination drift requires replanning,
not silently following a moved branch.

Before clean reconstruction, prepare the independent integration target as
new children of the pinned destination on a separate preparation line. Apply
only the mapped still-needed source intent, authorized fixes/extraction, and
planned adaptations. Skip fully ported or superseded work; for partially ported
changes apply only the unsupplied remainder. Verify destination implementations,
consumers, and tests support every skip and dependency substitution. A conflict,
empty patch, or matching subject does not prove equivalence. Uncertain or newly
discovered supersession returns to planning before dropping affected hunks.

Preserve destination fixes, intentional removals, compatibility, and migrations.
Do not restore the old full tree over the destination. When composing extraction,
exclude only the planned source contribution; removing destination-provided
behavior requires explicit scope. Audit destination-to-target and source-to-target
diffs against the mapping, separating inherited destination changes, skipped
source work, adaptations, and authorized fixes/exclusions. Run the relevant
integration/behavior checks, pin the verified target with a fresh immutable tag,
and record its exact identity as `EXPECTED_TIP`. Never copy the rebuilt tip to
prepare it. The old source and destination need not equal this tree; clean-to-
`EXPECTED_TIP` equality remains required. If nothing remains to port, validate
the destination as the target and result, accounting for every skipped change.

## Freeze the original

Use explicit revision expressions, preferably full commit IDs. Naming an
existing ref the user points at is fine. This workflow may create or move only
the new dedicated `CLEAN_BOOKMARK` and explicitly planned fresh residual bookmarks:

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

Verify the fresh tag from the source-fix phase, or create it if this execution
has not yet pinned its source. Keep its full commit ID for revset use:

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

For same-base reconstruction, verify the plan's longest initial prefix whose content, descriptions, and order
already fit the final plan. Record its full
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

When the duplicate's parent tree equals its source parent and the operation
preserves the complete source delta, its tree must match its source's:

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

Regardless of order, the clean tip's tree must match the recorded expected
target before cleanup continues:

```sh
jj diff --from "$EXPECTED_TIP" --to "$CLEAN_TIP" --summary
```

If the result is non-empty, stop. The wrong range, base, order, or mapping
was used.

If extraction leaves no suffix, validate `REBUILD_BASE` against `EXPECTED_TIP`
and account for every omitted source change. Report that base as `CLEAN_TIP`;
if a result bookmark is needed, create the fresh clean bookmark there after
validation. This is a verified extraction, not a history-only no-op.

## Mutation gate

Before every `jj abandon`, `absorb`, `describe`, `diffedit`, `duplicate`,
`new`, `resolve`, `restore`, `split`, or `squash`:

1. Resolve source and destination revisions explicitly. For `duplicate`, the
   destination must be `REBUILD_BASE` or the current clean tip. Reading or
   using a retained original as a parent is allowed; rewriting it is not.
2. Confirm every rewritten revision is in `NEW_STACK` or is an explicitly
   recorded temporary correction child owned by this reconstruction. A
   correction branch need not be an ancestor of the current clean tip.
   Planned residual branches have their own explicit owned revision sets and
   may be mutated under the same protections; never count them as `NEW_STACK`
   or use squash/absorb to move their behavior into the mainline.
3. Confirm no rewritten target intersects `OLD_STACK` or `BASE`. A parent
   used by `new` is read-only and may be `REBUILD_BASE`.
4. Prefer a narrow revision/path selection over `mutable()`, `all()`, or
   `mine()`.
5. For `resolve`, the target must be the temporary correction child, never
   a completed rebuilt commit. For `new`, verify its parent and preserve
   unrelated working-copy changes; do not insert it into original history.
6. For `restore`, confirm the intended state equality and inspect overwritten
   fixes and hunk ownership/timing as described in the reconstruction reference.

Useful checks (`CORRECTION_REVSET` and `RESIDUAL_REVSET` are the explicitly
recorded owned correction-child and residual sets, or `none()` when absent):

```sh
jj log -r "(<TARGET_REVSET>) & ($NEW_STACK | ($CORRECTION_REVSET) | ($RESIDUAL_REVSET))" \
  -T 'commit_id.short() ++ " " ++ description.first_line() ++ "\\n"'
jj log -r "(<TARGET_REVSET>) & ($OLD_STACK)"
```

The first should show every intended target; the second must be empty. If a
command refuses to rewrite a revision, stop and investigate. Do not bypass
immutability protection.

## Reference and publication rules

Never repoint, move, or delete a pre-existing bookmark or tag, and never
move the safety tag. Movable references are limited to the newly created
`CLEAN_BOOKMARK`, which must point to the current rebuilt tip, and planned fresh
residual bookmarks, each pointing to its validated branch tip. Never force-push
the clean stack over the original. Publishing, if requested, is a separate
explicit operation after validation.
