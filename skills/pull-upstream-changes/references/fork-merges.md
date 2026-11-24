# Merge upstream features into a fork

## Pin the target and map the overlap

Verify the upstream remote and fetch the requested branch or tag explicitly.
Record the original fork tip and the exact upstream target. Identify whether
the target is the fetched HEAD of the upstream branch being integrated, even
when the user named its commit ID. When the target is already reachable from
the fork, investigate any missing behavior as a downstream change or reversion.
When there is no common ancestor, verify the remote and history depth first.

Use `FORK` for the latest verified fork tip, `TARGET` for the pinned target, and
`NEXT` for a candidate checkpoint. In Git, map the first-parent timeline,
then inspect the full ancestry a candidate would add. Use the merge base of
`FORK` and `NEXT` as `BASE` for the path comparison.

```sh
git log --first-parent --reverse --oneline "$FORK..$TARGET"
git log --oneline "$FORK..$NEXT"
git merge-base --all "$FORK" "$NEXT"
git diff --name-status -M "$BASE" "$FORK"
git diff --name-status -M "$BASE" "$NEXT"
```

In Jujutsu, use `jj log -r "$FORK..$NEXT"` for new ancestry,
`jj log -r "heads(::$FORK & ::$NEXT)"` for merge bases, and
`jj diff --summary --from "$BASE" --to "$FORK"` and the corresponding diff to
`NEXT` for touched paths. If there are multiple bases, use the native merge
preview or candidate to see the actual overlap.

Check the candidate's full ancestry for feature prerequisites and unrelated
work. Every merge records that ancestry as integrated. If the requested
feature requires an out-of-scope ancestor, look for a narrower upstream ref.
If none exists, ask whether the user wants to expand scope or authorize a
different integration method.

## Choose the checkpoints

**A one-shot merge to upstream branch HEAD is forbidden, including for clean or
small updates.** Before creating any merge with the pinned branch HEAD as an
upstream parent, confirm that an earlier verified merge in this integration is
reachable from its fork-side parent. That earlier merge must have brought in a
previously absent, in-scope strict ancestor of HEAD. A downstream-only
preparation commit or a trial merge does not qualify. If no earlier checkpoint
meets these conditions, stop before merging HEAD and report the blocker.

1. Trace overlap in both paths and behavior. For a moved file, check the old
   and new paths and the callers. For an API or default change, find the first
   upstream revision with the new contract and the downstream consumers that
   rely on the old one, even if their files never overlap.
2. Cut at the first usable tree after a coherent prerequisite change and
   before the next change to the same area. For example, take a module move
   before a policy change inside the moved module. Resolve the fork's
   implementation into the new location once, smoke-test the existing
   behavior, then adopt the policy change using that resolved layout. Keep
   tightly coupled fixes with the transition they complete so each checkpoint
   can build and be tested. Skip transient API shapes that are replaced
   within the same upstream change.
3. For Git, compare a small number of candidate cuts with
   `git merge-tree --write-tree --name-only "$FORK" "$NEXT"` in the task repo.
   It can write Git objects and leaves the working tree and index alone. An
   exit status of 1 with listed paths indicates conflicts. Use the paths as
   a preview, then review the behavior changes. For Jujutsu, inspect conflicts
   in a task workspace draft at the chosen cut. Recompute the overlap from
   the last verified fork tip after each merge.
4. Record each upstream commit ID, the prerequisites it includes, the
   overlapping paths or contracts, and the smoke command and expected result.
   Use actual upstream commits as merge parents. For one advancing branch,
   each checkpoint should advance from the previous upstream ancestor toward
   the pinned target.

## Resolve and retain each merge

- **Git.** From the branch at `FORK`, run
  `git merge --no-ff --no-commit "$NEXT"` after checking the HEAD rule. List
  unresolved paths with `git diff --name-only --diff-filter=U`. For a textual
  conflict, `git ls-files -u -- "$FILE"` shows the available stages. Inspect
  stages 1, 2, and 3 with `git show ":1:$FILE"`, `git show ":2:$FILE"`, and
  `git show ":3:$FILE"` where present. Stage the resolution, then review
  `git diff --cached` and make sure the tested files match the staged tree.
  Commit when the smoke checks pass and the unmerged-path list is empty.
- **Jujutsu.** Run `jj new "$FORK" "$NEXT" -m "$MESSAGE"` after checking
  the HEAD rule. Use `jj status` and `jj resolve --list` to locate conflicts.
  Inspect the same file at the merge base and both parents with
  `jj file show -r "$REV" "$FILE"` where present. Review the candidate with
  `jj diff --from "$FORK" --to @`. Confirm that
  `jj log --no-graph -r 'conflicts() & @'` lists no revisions. Commit with
  `jj commit -m "$MESSAGE"` after the smoke checks pass and advance the task
  bookmark to the completed merge. Keep Git index operations out of jj.
- Keep the verified merge as the fork-side parent of the next step. If a
  candidate mixes distinct transitions or repeatedly conflicts on code about to
  move, reconsider the cut from the last verified tip. In Git, use
  `git merge --abort` for the task-owned in-progress merge before changing
  cuts. In jj, start the replacement from the last verified bookmark and
  retain the failed draft if it contains useful resolutions.

## Verify behavior and ancestry

For example, if the fork uses a ten-second timeout, the first merge moves its
implementation and the second introduces retries with a new timeout default.
Run the same consumer test, such as
`cargo test -p client --test upstream_smoke preserves_fork_timeout`, before
integration and after both merges. It should assert ten seconds through the
public client. At the second merge, also test that retries work. A result of
thirty seconds after a clean merge means the second candidate still needs a
fix. Keep the first verified merge reachable while fixing and retesting the
second.

Inspect the final parents and ancestry. In Git, use `git show -s --format=%P`
on each merge and `git merge-base --is-ancestor` to verify that the earlier
merges and approved upstream commits are reachable. In jj, inspect the
parents with `jj log -r "$MERGE-"` and check reachability in the final
revision's ancestors with `jj log -r "$MERGE & ::$FINAL"`. Check the list of
added commits against the approved scope, then run the affected final checks.
Report each merge's two parents and its smoke result with the integration tip.
