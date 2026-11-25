---
name: jj-development-workflow
description: >
  Run quick, append-only development or review and targeted fixes in a Jujutsu
  workspace. Use when starting or resuming a jj development stack, applying
  review fixes, or reusing and retiring development workspaces.
license: MIT
---

# JJ Development Workflow

Use **quick development** to build and document a stack incrementally. Use
**review and fix** to investigate an existing revision or stack and apply
authorized repairs. Both modes preserve completed changes and can use an
isolated `jj workspace` when needed. A review-only request ends with findings.
Restacking, folding patches, and publishing have their own scope.

## Choose a workspace

Get explicit user approval before affecting another workspace you did not
create. Name the workspace and describe the expected effect. Before rewriting
a revision, compare it and its descendants with the registered workspace heads.
A rewrite can move those heads even when run from a separate checkout.

1. Identify the repository with `jj root`. Inspect relevant revisions and
   registered workspaces with `jj --ignore-working-copy --no-pager log` and
   `jj --ignore-working-copy --no-pager workspace list` from the source
   checkout. Branch from the agreed integration base
   for independent work, the current completed stack tip for a continuation,
   or the exact source revision for an isolated review or benchmark. For
   stacked fixes, choose the reviewed tip that contains the dependencies
   the fixes need. Resolve and record the base change ID and commit ID.
2. Use one task workspace for serial work. Resume ongoing work and make
   follow-up amends in that workspace. For a new task, reuse an available
   workspace already on the intended base, including `default` when it fits.
   Confirm who owns other candidates before choosing one.
   An unrelated workspace can hold work even when its working copy is clean.
   If the current workspace is on a feature branch and the task starts from
   trunk, leave that checkout in place and use a workspace based on trunk.
3. If no available workspace is already on the intended base, create one there.
   Use the repository's workspace convention or choose a stable name and a
   dedicated path outside build and cache directories. Run the command from a
   clean task checkout. It can snapshot the source and requires working-copy
   access. If only another workspace you did not create is available as the
   source, get approval before running the command there. Disclose any pending
   edits that the command could snapshot.

   ```sh
   jj workspace add --name <name> -r <base-commit-id> <path>
   ```

   Use `--no-colocate` when Git worktree integration is unnecessary.
4. Verify `jj root` and the parent in the selected workspace. Use
   `--ignore-working-copy` when inspecting other workspaces. Before starting a
   new task, verify an empty, conflict-free change with `jj --no-pager status`
   and `jj --no-pager diff --summary`. Account for generated or untracked files
   that jj might ignore. Edit only the working-copy change assigned to the task
   or your own in-progress work. Commit unfinished work only when its
   checkpoint is in scope and the description records its status.

## Quick development

- Append a coherent change for each increment or meaningful checkpoint. Use
  a new change for follow-ups, including corrections to your earlier commits.
  Preserve all finished commits and descriptions. Keep amendments, rebases,
  squashes, absorbs, and abandonment of completed revisions outside this mode.
  Moving to a newer integration base or cleaning up history is a separate task.
- Choose each description by intended use. Follow the message guidance in
  `jj-commit` when available.
  - **Land independently.** Explain the delivered behavior, motivation, and
    consequential design decisions. Keep progress, blockers, integration
    instructions, and routine checks in the handoff.
  - **Amend, fold, or replace later.** Reference the step-by-step plan when
    available and identify the step covered. Record progress and verification
    so far, findings, deviations, blockers, and the next step. State the
    intended disposition, including a named decision when integration is
    pending. Use stable jj change IDs for dependencies and fold targets. If a
    later checkpoint changes the disposition or resolves a blocker, record the
    update there.
  - **Explore.** Start from the goal or question and choose how to investigate
    when the method is open. Record the approach actually tried and the results.
    For runtime, compile time, or other comparisons, identify the exact baseline
    and candidate revisions, the conditions, values, units, and observed change.
    Note inconclusive or unavailable measurements and point to retained outputs
    when available.

## Review and fix

- Review the specified revision or range directly. If checks require a
  checkout, reuse an available workspace at the revision under review.
  Check design adoption, behavior, regressions, and dependencies. Tie each
  finding to the responsible change and affected behavior. Skip formatting
  and linter checks during review.
- For each authorized fix, append a narrowly scoped change on a base that
  reproduces the issue and contains the needed dependencies. Group findings
  only when the same correction resolves them. Keep unrelated repairs in
  their own changes and leave reviewed revisions intact.
- Verify the behavior that exposed the defect against the repaired tree.
  Explain the defect and what makes the fix sufficient. For a fix intended to
  fold, also record the affected change ID, fold target, and any dependencies
  that constrain where it can land.

## Finish each change

For agent-made changes, record agent identity in the commit message only for
quick development checkpoints and exploration.

1. Inspect the task diff and verify the relevant behavior. `jj fix` is
   allowed on your own in-progress change. Scope it explicitly with
   `jj fix -s @ <paths>` after checking that `jj log -r '@+'` is empty.
   The command can affect descendants, and the default source can include
   other mutable revisions. Keep the configured tool's in-scope edits and
   review them with the task diff. Avoid spending time reverting acceptable
   formatter churn line by line. Recheck affected behavior after it runs.
2. Commit the current change with `jj commit -m <complete-description>`
   using literal multiline text. Serialize mutations to shared repository
   state, even across workspaces. Review the saved description and completed
   diff. Verify a clean working copy before handoff with `jj --no-pager status`
   and `jj --no-pager diff --summary`. Check for conflicts and unexpected
   untracked files. Preserve and report any unrelated edits.

## Retain one task workspace at handoff

Keep the main task workspace available after handoff so the user can request
follow-up edits or an amend. Leave its removal to the user unless they
explicitly ask you to remove it.

Create additional workspaces only for parallel work. Designate the extras you
create as disposable at creation. Keep reports, benchmark data, and other
outputs to retain outside them. Remove the disposable workspaces before
reporting completion so exactly one workspace remains for the task. Leave
unrelated workspaces in place.

Use this procedure to remove a disposable checkout you created or a workspace
whose removal the user explicitly requested.

1. Move any outputs to retain outside the workspace, stop tools using the
   checkout, and account for pending tracked, untracked, and ignored files.
   Commit work that belongs in history before cleanup. Leave a clean working
   copy and check that the retained commits are reachable in the shared repo.
   If a stack has no durable ref, create a uniquely named local bookmark at
   its completed tip with `jj bookmark create <name> -r <tip>`. A single
   bookmark covers the completed ancestors on that stack.
2. From a clean workspace you are keeping, verify the registered name and
   resolved absolute path of the checkout selected for removal. Run
   `jj workspace remove <name>` to unregister it and delete its directory.
   This removes ignored and untracked files in that directory as well.
3. Check that the registration and directory are gone and the retained tip
   still resolves. At handoff, verify that only the retained task workspace
   remains, or that its removal was requested and completed. Hand off the
   base and completed change IDs, the bookmark if used, and the location of
   any retained artifacts.
