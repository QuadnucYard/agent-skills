# Command Recipes

Replace uppercase revision labels with **recorded IDs**. Capture new change IDs
from command output; re-resolve exact revisions after rewrites. `FINAL` is the
pinned source snapshot and `BASE` the parent of the unit being split. Commands
below operate on **new, workflow-owned changes**.

## Paths that reach their final state

Use **restore for state equality**, not to replay a patch. Check the source
timeline: every selected path must already have its final content at this step,
with **no later edits, renames, deletions, or unrelated hunks** in that path.

```sh
jj --no-pager new BASE -m "purpose and motivation"
jj --no-pager restore --from FINAL --into STEP path/to/file other/path
jj --no-pager diff -r STEP --git
```

Validate `STEP` before building its child. For shared files with later changes,
**manually reconstruct** the intended state or use an earlier source milestone.

## Small early commits

Build the small parts directly, including their integration and tests:

```sh
jj --no-pager new BASE -m "early purpose and motivation"
# Manually edit and validate this milestone, then record its ID as EARLY.
jj --no-pager new EARLY -m "remaining purpose and motivation"
jj --no-pager restore --from FINAL --into LAST
jj --no-pager diff -r LAST --git
```

Repeat the manual step for additional early parts. Restore the complete tree
only at the **last planned residual**; check that its diff is one coherent
purpose. Partition further if it still mixes concerns. For multiple source
commits, retain meaningful intermediate states rather than jumping over them.

## Large early commits: subtract and invert

Let the source delta be **A + B**, where **A goes first**. Algebraic labels denote
changes, not literal concatenation; overlapping edits may require resolution.

1. **Duplicate** the source unit onto `BASE`; record the duplicate as `D`.

   ```sh
   jj --no-pager duplicate SOURCE --onto BASE
   jj --no-pager new D -m "temporary subtraction of A"
   ```

   Manually remove **A**, leaving the residual state **B**. Snapshot with
   `jj --no-pager diff --git`; record this child as `MINUS`. Its delta must be
   exactly **-A**, including A's tests and integration.

2. **Invert the subtraction** onto `BASE` to extract **A**:

   ```sh
   jj --no-pager revert --revision MINUS --onto BASE
   ```

   Record the result as `A`. If shared-file context conflicts, reconstruct the
   intended A milestone in a correction child and squash that correction into
   `A` with `--use-destination-message`. **Validate A against BASE** before
   continuing; successful patch application alone is insufficient.

3. **Invert A on top of itself**, then fold the full duplicate into that inverse:

   ```sh
   jj --no-pager abandon MINUS
   jj --no-pager describe -r A -m "early purpose and motivation"
   jj --no-pager revert --revision A --onto A
   ```

   Record the inverse as `UNDO_A`. Its tree must equal `BASE` before proceeding.

   ```sh
   jj --no-pager diff --from BASE --to UNDO_A --summary
   jj --no-pager squash --from D --into UNDO_A -m "remaining purpose and motivation"
   ```

   The squash consumes `D`; its full delta cancels **-A**, leaving **B** on A.
   Record the rewritten `UNDO_A` as `RESULT`. Require **BASE → A → B**, no helper
   commits in that line, and an empty source-to-result tree comparison. Review
   and validate B independently; rewrite its description to exclude A's work.

For **multiple sources**, duplicate the first onto `BASE` and each next source
onto the previous copy. Squash those owned copies into one `D` whose parent is
`BASE` and tree equals the unit's final state. Do this only when collapsing their
intermediate states is justified; otherwise split milestone by milestone.
For **more parts**, repeat on the residual with the validated prefix as the new
base. Temporary B-only states need not build; all surviving milestones must.

See the official [jj command reference](https://docs.jj-vcs.dev/latest/cli-reference/)
and installed help for `restore`, `duplicate`, `revert`, and `squash` semantics.
