---
license: MIT
name: jj-patch-stack
description: Create additive Jujutsu patch changes for existing revisions while preserving original history, then provide a guide to squash approved patches into their targets. Use when fixes must be layered from oldest to newest and applying them requires separate approval.
---

# JJ Patch Stack

Patch existing revisions by adding new `jj` changes. Keep original changes untouched during preparation, and finish with concrete instructions for applying the patches after approval. Preparing or approving patch content does not authorize applying it; execute the squash guide only when the user explicitly authorizes that history rewrite.

## Non-Negotiable Rules

These rules govern patch preparation. "Apply After Approval" permits only the described squash operations and their automatic descendant rewrites after explicit authorization; all other prohibitions remain in force.

- Use `jj` only. Do not run any `git` command.
- Do not run `jj squash`, `jj rebase`, `jj abandon`, `jj restore`, or `jj undo`.
- Never directly edit an already-built change, including your committed patches. Do not use `jj edit` to check out and modify an existing revision. Make corrections in a new additive patch on top of the affected patch; never squash it into an existing change. The only revision you may edit directly is the new patch change under construction while it is `@`.
- Original targets and committed patches keep the same change ID and commit ID throughout. Corrections remain separate additive patches.
- Process target revisions from oldest to newest.
- Each patch after the first must have both the current target and the previous patch as parents. This carries the complete patch stack forward without changing either parent.
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

## Workflow

1. Run `jj status` and inspect the relevant graph with `jj log`. Preserve unrelated work. If the working copy contains changes whose ownership is unclear, stop and ask before proceeding.
2. Identify every target revision and order them by ancestry, oldest first. If the order is ambiguous, do not guess.
3. For the oldest target, call the immutable revision `target-1` and create a child:

   ```text
   jj new target-1
   ```

4. Make only the fix for `target-1`, format the content and description per "Well-Formed Commits", run focused verification, inspect the diff, and commit it with a well-formatted description:

   ```text
   jj diff
   jj commit -m "<patch description>"
   ```

   Record the committed patch's change ID as `patch-1`. After `jj commit`, this is normally the revision at `@-`; confirm it with `jj log` rather than relying on memory.

5. For the next immutable target, call it `target-2`. Create a merge change whose parents are `target-2` and the previous patch `patch-1`:

   ```text
   jj new target-2 patch-1
   ```

6. Inspect the new working-copy change. Resolve conflicts brought forward from `patch-1` here, then make the fix for `target-2`. Do not alter either parent.

   Use `jj status` to find conflicted files and `jj resolve` (or the repository's normal file-level resolver) while `@` is the new patch. Re-run the focused checks after every conflict is resolved.
7. Verify, inspect, and commit this new patch with a well-formatted description (see "Well-Formed Commits"). Record its change ID as `patch-2`; it becomes the previous patch for the next iteration.
8. Repeat steps 5-7 for every remaining target. For iteration `n`, use immutable `target-n` and the latest additive `patch-(n-1)` as the two parents, then record the new result as `patch-n`.
9. Finish preparation with `jj status`, `jj log`, and focused diffs/tests. Confirm that every original target still has the same change ID and commit ID and that the final patch contains all earlier fixes.
10. Deliver the application guide described below, using the actual patch and target IDs. Leave the patches separate unless applying them has been explicitly authorized.

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

Always include a squash guide in the patch handoff. List every patch, including corrective patches, its original destination target, both revisions' full change IDs and current commit IDs, and the checks already run. Record the final reviewed patch tip's full commit ID for the final tree comparison. Provide concrete commands with those change IDs substituted for the labels below; do not execute them merely because the user requested patches or approved their content.

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
