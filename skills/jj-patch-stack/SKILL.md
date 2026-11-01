---
license: MIT
name: jj-patch-stack
description: Create additive Jujutsu patch graphs for fixes, redistribution of top changes, and insertion of new changes between existing revisions while preserving original history. Validate the intended final stack through a mapping to the graph without rebuilding it; provide squash instructions for patches that fold into existing targets.
---

# JJ Patch Stack

Represent fixes and new changes by adding `jj` changes while keeping original history untouched. The deliverable is a patched graph with a complete mapping to the intended final stack; constructing that final stack is not required. Include concrete squash instructions for patches intended to fold into existing targets. Preparing or approving patch content does not authorize applying it; execute the squash guide only when the user explicitly authorizes that history rewrite.

One goal is to prepare the absorption or dissolution of changes collected at the top of a stack into the earlier revisions that own them, without rewriting history during preparation. Reconstruct those changes as additive patches; keep the original top changes intact as source evidence. Folding patches into existing revisions belongs to the separately authorized application phase. Removing source changes is outside that phase's squash-only permission and requires its own explicitly authorized scope.

## Non-Negotiable Rules

These rules govern patch preparation. "Apply After Approval" permits only the described squash operations and their automatic descendant rewrites after explicit authorization; all other prohibitions remain in force.

- Use `jj` only. Do not run any `git` command.
- Do not run `jj squash`, `jj rebase`, `jj abandon`, `jj restore`, or `jj undo`.
- Never directly edit an already-built change, including your committed patches. Do not use `jj edit` to check out and modify an existing revision. Make corrections in a new additive patch on top of the affected patch; never squash it into an existing change. The only revision you may edit directly is the new patch change under construction while it is `@`.
- Original targets, source top changes, and committed patches keep the same change ID and commit ID throughout. Corrections remain separate additive patches.
- Process target revisions from oldest to newest.
- When carrying an existing target forward after an earlier prepared prefix, create a merge change with that target and the latest prepared prefix as parents. An inserted standalone change instead has the latest prepared prefix as its parent. Both forms carry earlier prepared work forward without changing existing parents.
- Resolve inherited merge conflicts only in the newly created patch change.
- Format every command, flag, revision name, and change or commit ID as code: inline backticks in prose, fenced `sh` blocks for command sequences. Never leave code unformatted.
- Every commit this workflow creates must be well formatted: formatted content and a proper description, per "Well-Formed Commits" below.
- If the requested result cannot be produced without a forbidden operation, stop and explain the constraint.

Read-only commands such as `jj status`, `jj log`, `jj show`, and `jj diff` are allowed. Additive commands such as `jj new`, `jj describe`, `jj commit`, and conflict-resolution commands are allowed only when they operate on the new patch change.

## Well-Formed Commits

A patch change must be complete and well formatted before you commit it and move on to the next target.

- Content: run the repository's formatter and linters on the changed files (for example `cargo fmt --check` and `cargo clippy` in a Rust repo) and fix any findings inside the same new change before committing. Never commit knowingly unformatted or failing code.
- Description: follow the repository's commit-message convention — check recent subjects with `jj log` to detect it (for example Conventional Commits). Use a concise, imperative subject line, and a body only when the reasoning is not obvious from the diff. Never leave the description empty or placeholder.
- A committed patch is an existing change: never edit it in place. If a check problem appears after committing, create a new additive patch on top, fix it there, verify, and commit it separately.

## Examples and Strategy Selection

Choose the strategy by ownership and dependencies, rather than assuming every fix is a direct copy of a diff. These examples illustrate different cases; they are not an exhaustive list of supported fixes.

- **A new bug fix:** an earlier revision introduces an incorrect boundary check, but no fix exists yet. Implement the correction and its regression test in a new child of that target, then carry it forward through the later targets.
- **A fix already collected at the top:** a top change repairs a parser introduced earlier. Reconstruct the parser fix and its test in a patch on the owning revision. Preserve the top change; do not invoke `jj absorb` or move its contents out of it during preparation.
- **Several independent fixes in one top change:** the top change repairs both parsing and caching introduced by different revisions. Separate the fixes by behavior and ownership, even when they touch the same file, then build patches from the older target to the newer one.
- **A fix with a prerequisite:** a top fix calls a helper introduced only in a later revision. Either express the fix using the earlier revision's existing facilities and adapt it later, or place it at the earliest target where the required behavior and helper coexist. Do not copy an unrelated later feature into an earlier target merely to make the patch compile.
- **A fix that changes shape across the stack:** an early correction touches an API that a later target renames or replaces. Implement the correction against the early API, then resolve the inherited conflict and preserve the same behavior in the new patch on the later target. An automatically merged result still needs behavior checks.
- **A partially redundant or mixed top change:** some top edits are already satisfied by earlier patches, while others introduce an independent feature. Do not duplicate the satisfied edits or silently discard the feature. Record which edits are covered and keep the remaining feature as an explicit residual change or separate follow-up scope.
- **A new change between existing revisions:** the intended order is `target-1`, `insert-1`, then `target-2`. Create `insert-1` on the prepared state of `target-1`, then merge the unchanged `target-2` with `insert-1` in a new carry-forward change. Keep `insert-1` as a standalone final change rather than treating it as a fix to squash into either neighbor. Resolve any interaction with `target-2` in the carry-forward change. Repeat for multiple insertions at any boundary.

For existing top changes, record the source commit IDs, map each relevant behavior to its target, and account for any residual work. Build from the intended targets, using the source changes as references rather than adding them as parents and inheriting all their edits. For pure redistribution, compare the completed patch tip's tree with the original source tip's tree; they should match. If additional fixes or excluded work intentionally change the result, explain those differences and verify the intended behavior instead of claiming tree equality. Include any retained source changes and residual work in the application guide so that later integration does not apply the same fix twice.

## Mapping Validity Without Rebuilding

A patch graph is valid when every change in the intended final stack can be mapped from it. Record the final order and, for each entry, its role (unchanged target, patched target, or standalone insertion), the graph revisions representing it, the cumulative tree after it, and the intended delta from the preceding mapped tree. Record full change and commit IDs so the mapping identifies the reviewed graph precisely. The graph's merge topology does not have to be the intended final stack's linear topology.

For example, with original history `target-1 -> target-2 -> target-3`, prepare an insertion as follows; the arrows here denote the intended oldest-to-newest order:

```text
insert-1 = new(target-1)
carry-2 = new(target-2, insert-1)
carry-3 = new(target-3, carry-2)
```

| Intended final change | Mapped cumulative tree | Delta to review |
| --- | --- | --- |
| `target-1` | `target-1` | Original `target-1` delta |
| Standalone `insert-1` | `insert-1` | `target-1` to `insert-1` |
| Adapted `target-2` | `carry-2` | `insert-1` to `carry-2` |
| Adapted `target-3` | `carry-3` | `carry-2` to `carry-3` |

Review each mapped delta against its intended behavior and dependencies, and verify each mapped cumulative tree is conflict-free and passes its focused checks. For carry-forward merges, review the delta from the preceding mapped prefix, not only the merge's own diff: the final change also includes the original target's contribution. Account for all requested changes and any intentionally excluded or residual work. Tip-tree equality alone cannot establish valid intermediate boundaries.

Once this mapping is complete and verified, preparation is complete. Do not rebuild a separate linear stack, rebase existing revisions, or fold an insertion into a neighbor merely to demonstrate that the mapping can be realized. If a mapped boundary is missing or invalid, add or correct it through a new additive change and update the affected mappings. Retain this criterion for combinations of fixes, insertions, redistribution, and later extensions of the graph.

## Workflow

1. Run `jj status` and inspect the relevant graph with `jj log`. Preserve unrelated work. If the working copy contains changes whose ownership is unclear, stop and ask before proceeding.
2. Identify every target revision and order them by ancestry, oldest first. Record any standalone insertions at their intended boundaries in the final order. If the order is ambiguous, do not guess. When fixes already exist in top changes, map their ownership, dependencies, and residual work as described in "Examples and Strategy Selection" before constructing patches.
3. For the oldest target, call the immutable revision `target-1`. If it needs no fix, use it directly as the prepared prefix and proceed to the next insertion or target. Otherwise create a child:

   ```text
   jj new target-1
   ```

4. When constructing a fix patch, make only the fix for `target-1`, format the content and description per "Well-Formed Commits", run focused verification, inspect the diff, and commit it with a well-formatted description:

   ```text
   jj diff
   jj commit -m "<patch description>"
   ```

   Record the committed patch's change ID as `patch-1`. After `jj commit`, this is normally the revision at `@-`; confirm it with `jj log` rather than relying on memory.

5. Before advancing to the next immutable target, create any planned standalone insertions in order, each with the latest prepared prefix as its parent. Verify and commit each insertion before proceeding; the committed insertion becomes the new prefix. Call the next immutable target `target-2`. Create a merge change whose parents are `target-2` and the latest prepared prefix. Without an intervening insertion, when that prefix is the previous patch `patch-1`, this is:

   ```text
   jj new target-2 patch-1
   ```

6. Inspect the new working-copy change. Resolve conflicts brought forward from the prepared prefix here, then make any fix for `target-2`. A carry-forward change may need no additional edits. Do not alter either parent.

   Use `jj status` to find conflicted files and `jj resolve` (or the repository's normal file-level resolver) while `@` is the new patch. Re-run the focused checks after every conflict is resolved.
7. Verify, inspect, and commit this new patch with a well-formatted description (see "Well-Formed Commits"). Record its change ID as `patch-2`; it becomes the previous patch for the next iteration.
8. Repeat steps 5-7 for every remaining target. At each planned insertion boundary, create and verify a new standalone change on the latest prepared prefix; it becomes the prefix for the next insertion or target. For the next existing target, use immutable `target-n` and that latest prefix as the two parents. Create carry-forward changes even for targets requiring no new fix when they are needed to represent a later mapped boundary. Original unchanged prefixes may be mapped directly without creating empty fix changes.
9. Finish preparation with `jj status`, `jj log`, and focused diffs/tests. Verify the complete final-stack mapping as described above, confirm every original target and source change retains its change and commit IDs, and check the final mapped tree contains all intended earlier work. Do not construct a separate final stack for this validation.
10. Deliver the verified mapping and the applicable application guide described below, using actual revision IDs. Leave the graph intact unless applying changes has been explicitly authorized.

## Shape of the History

For immutable targets `target-1`, `target-2`, then `target-3`:

```text
patch-1 = new(target-1)
patch-2 = new(target-2, patch-1)
patch-3 = new(target-3, patch-2)
```

- `patch-1` is the new patch on `target-1`.
- `patch-2` is a new merge patch on both `target-2` and `patch-1`.
- `patch-3` is a new merge patch on both `target-3` and `patch-2`.

The original target line remains intact. Continue the same pattern for any number of future targets.

## Apply After Approval

Always hand off the verified final-stack mapping and checks already run. For patches that fold into existing targets, include a squash guide listing every such patch, including corrective patches, its original destination target, and both revisions' full change IDs and current commit IDs. Record the final reviewed graph tip's full commit ID for the final tree comparison. Provide concrete commands with those change IDs substituted for the labels below; do not execute them merely because the user requested patches or approved their content.

Standalone insertions have no squash destination. Mark them as retained final changes and distinguish carry-forward nodes from fix patches in the mapping. The squash-only procedure below applies when the complete intended result can be obtained by folding patches into existing targets; it does not materialize standalone insertions between targets. For a graph containing insertions, the verified mapping is a sufficient completed deliverable. Do not rebuild it or invent a squash destination for an insertion. Any later request to materialize that final order needs an explicitly authorized scope covering the required history operations.

Explain that applying the patches rewrites target and descendant commit IDs, automatically rebases descendants, and normally abandons emptied patch changes. Target change IDs remain usable across these rewrites. This ends the preparation phase's commit-ID preservation guarantee. Approval must cover the affected history; it does not authorize pushing or bypassing configured immutable revisions.

Once application is authorized:

1. Recheck `jj --no-pager status` and the relevant `jj --no-pager log`. Confirm that the patch/target mapping still matches the reviewed commit IDs, inspect affected descendants and bookmarks, and preserve unrelated working-copy edits. If the reviewed content or rewrite scope changed, refresh the guide and obtain approval for that change before applying. Record the pre-application operation ID with `jj --no-pager op log --limit 1` for recovery; do not run recovery commands automatically.
2. Squash from the oldest target to the newest, one explicit source/destination pair at a time:

   ```sh
   jj --no-pager squash --from patch-1 --into target-1 --use-destination-message
   jj --no-pager squash --from patch-2 --into target-2 --use-destination-message
   jj --no-pager squash --from patch-3 --into target-3 --use-destination-message
   ```

   `patch-n` and `target-n` stand for the recorded change IDs. Use change IDs for these commands because earlier squashes change later commit IDs. Do not use bare `jj squash` or `jj squash -r patch-n`: later patches have multiple parents, and their destination must be explicit. Each command moves that patch's own delta; inherited earlier fixes move with the earlier target rewrites. Do not squash every patch into the final target.

   For a single target, run only its pair. For additional targets, extend the sequence in the same order. Fold a patch and then its corrective patches, in dependency order, into the same original target before moving to the next target; never use an emptied patch as the destination. Keep the target description with `--use-destination-message`, or replace that flag with `-m "<complete updated target description>"` when the approved fix changes the target's intent.
3. After each squash, inspect the rewritten target and pending patches with `jj --no-pager log`, `jj --no-pager show -r target-n`, and focused diffs. Re-resolve the remaining change IDs before continuing; stop if a source or destination is missing, divergent, or ambiguous. An early squash can temporarily conflict in a later target whose approved patch already carries the resolution. Continue only when that resolution is accounted for in the next planned squashes; stop on unexpected conflicts rather than inventing new fixes. Each target must be conflict-free and pass its focused checks after all its patches have been folded.
4. After the last squash, verify that the rewritten final target has exactly the reviewed final patch tree:

   ```sh
   jj --no-pager diff --from <reviewed-tip-commit-id> --to <final-target-change-id>
   jj --no-pager log -r 'conflicts() & ancestors(<final-target-change-id>)'
   jj --no-pager status
   ```

   The diff and conflict query must be empty. Use the saved full commit ID for the reviewed tip, since its patch change may now be abandoned. Run the relevant behavior checks again, verify target descriptions and affected bookmarks/descendants, and report the rewritten target IDs and results. If validation fails, stop and report it; do not silently restore, undo, or create additional fixes under the squash approval.

The explicit source/destination flags and noninteractive description options are documented in the [Jujutsu squash reference](https://docs.jj-vcs.dev/latest/cli-reference/#jj-squash). Check `jj --no-pager squash --help` for the installed version before applying.
