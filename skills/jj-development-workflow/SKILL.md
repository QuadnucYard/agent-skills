---
name: jj-development-workflow
description: >
  Run quick, append-only development or review and targeted fixes in a Jujutsu
  workspace. Use when starting or resuming a jj development stack, applying
  review fixes, or retiring a temporary checkout while retaining its history.
license: MIT
---

# JJ Development Workflow

Use **quick development** to build and document a stack incrementally. Use
**review and fix** to investigate an existing revision or stack and apply
authorized repairs. Both modes use an isolated `jj workspace` and preserve
completed changes. A review-only request ends with findings. Restacking,
folding patches, and publishing are distinct operations with their own scope.

## Start in a clean workspace

1. Identify the repository with `jj root`. Inspect relevant revisions and
   registered workspaces with `jj --ignore-working-copy --no-pager log` and
   `jj --ignore-working-copy --no-pager workspace list` from the source
   checkout. Branch from the agreed integration base
   for independent work, the current completed stack tip for a continuation,
   or the exact source revision for an isolated review or benchmark. For
   stacked fixes, choose the reviewed tip that contains the dependencies
   the fixes need. Resolve and record the base change ID and commit ID.
2. Use a dedicated path and unique name. Follow the repository's workspace
   convention. Otherwise use a sibling checkout or an ignored workspace area
   owned by the repository. Confirm the destination is available and outside
   any directory that build or cache cleanup can erase. If the repository
   intentionally keeps workspaces under a build directory, avoid cleanup
   commands that would delete those checkouts. Put reports, benchmark data,
   logs, and other artifacts that must survive in a durable location outside
   the temporary workspace.
3. Create the workspace from a clean checkout of the same repository, with
   the recorded commit as its explicit parent. Workspace creation can
   snapshot the source checkout. If the source has pending edits, use
   another clean checkout or coordinate with the owner to finish those
   edits first. Verify `jj root` and the parent once inside, and run task
   edits and commands there.

   ```sh
   jj workspace add --name <name> -r <base-commit-id> <path>
   ```

   Use `--no-colocate` when Git worktree integration is unnecessary.
4. Before starting each new task, require an empty, conflict-free working-copy
   change. Check `jj --no-pager status` and `jj --no-pager diff --summary`,
   and account for generated or untracked files that jj might ignore.
   Snapshot only a workspace assigned to the task. If a proposed workspace
   contains unrelated edits, leave them with their owner and create a fresh
   workspace from the intended committed base. Edit only the working-copy
   change you created for the task or can establish as your own in-progress
   work. Commit unfinished work only when its checkpoint is in scope and
   the description records its status.

## Quick development

- Append a coherent change for each increment or meaningful checkpoint. Use
  a new change for follow-ups, including corrections to your earlier commits.
  Preserve all finished commits and descriptions. Keep amendments, rebases,
  squashes, absorbs, and abandonment of completed revisions outside this mode.
  Moving to a newer integration base or cleaning up history is a separate task.
- Expect the development stack to include changes with different destinations.
  Write the purpose, impact, and dependencies in each change's description,
  followed by the agent identity if an agent made the commit. Record the
  intended disposition for trunk, such as land independently, fold into
  change `<change-id>`, replace before landing, keep as an experiment outside
  trunk, or pending a named decision. These are instructions for the eventual
  integration, carried in the description.
- Record progress a reviewer needs, including key decisions, limitations,
  behavior verified, and remaining work or checks. Use stable jj change IDs
  for dependencies, superseded work, and fold targets. Record an exact commit
  ID when the evidence depends on a specific tree. If a later change alters
  a prior disposition or resolves a limitation, record that update in the
  later description.

## Review and fix

- Review the specified revision or range in a dedicated workspace. Check
  design adoption, behavior, regressions, and dependencies. Tie each finding
  to the responsible change and affected behavior. Skip formatting and
  linter checks during review.
- For each authorized fix, append a narrowly scoped change on a base that
  reproduces the issue and contains the needed dependencies. Group findings
  only when the same correction resolves them. Keep unrelated repairs in
  their own changes and leave reviewed revisions intact.
- Verify the behavior that exposed the defect against the repaired tree.
  Record the finding, affected change ID, what makes the fix sufficient, and
  intended integration. If the fix only works with later dependencies,
  record those dependencies before proposing a fold into an earlier change.

## Finish each change

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
   diff. Check `jj --no-pager status` and `jj --no-pager diff --summary`
   again. The new working copy must be empty and conflict-free, with any
   leftover files accounted for.

## Retire temporary workspaces

Clean up task-owned temporary workspaces as soon as their purpose ends,
including short-lived benchmark or comparison checkouts.

1. Move any outputs to retain outside the workspace, stop tools using the
   checkout, and account for pending tracked, untracked, and ignored files.
   Commit work that belongs in history before cleanup. Leave a clean working
   copy and check that the retained commits are reachable in the shared repo.
   If a stack has no durable ref, create a uniquely named local bookmark at
   its completed tip with `jj bookmark create <name> -r <tip>`. A single
   bookmark covers the completed ancestors on that stack.
2. From a clean workspace you are keeping, verify the registered name and
   resolved absolute path of the task-owned checkout. Run
   `jj workspace remove <name>` to unregister it and delete its directory.
   This removes ignored and untracked files in that directory as well.
3. Check that the registration and directory are gone and the retained tip
   still resolves. Hand off the base and completed change IDs, the bookmark
   if used, and the location of any retained artifacts. Leave the primary
   workspace and existing refs alone.
