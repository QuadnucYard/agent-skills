---
name: pull-upstream-changes
description: >
  Integrate upstream features into a fork with Git or Jujutsu merges, or
  update Rust crate dependencies and migrate callers to upstream API changes.
  Use when a project needs to adopt upstream work and verify that its own
  behavior survives the integration.
license: MIT
---

# Pull Upstream Changes

- For a fork, read [fork merges](references/fork-merges.md). Select upstream
  checkpoints by the features, prerequisites, and ancestry they bring in.
  A one-shot merge to upstream branch HEAD is forbidden. Merge HEAD only
  after a verified merge in the same integration has brought in an earlier
  in-scope ancestor of HEAD.
- For a Rust dependency, read [Cargo API migrations](references/cargo-api-migrations.md).
  Update the dependency and migrate its callers as one verified change.
- When both apply, order the merges and migrations by their prerequisites. Group
  coupled changes into a checkpoint if neither part can work independently.

## Establish the baseline

Identify the requested upstream behavior, the downstream guarantees to preserve,
and any approved behavior changes. Resolve exact starting and target revisions
or package versions and sources. Use a task-owned worktree or workspace at the
recorded downstream revision. In a Jujutsu repository, use `jj` for mutations and
reuse an available workspace already at the intended base or create one there
from a clean task checkout. Get explicit user approval before affecting another
workspace you did not create. Keep the task workspace for follow-up merges.

Pick a quick smoke test through an affected consumer or public entry point. Reuse
existing checks that assert the relevant outputs, state changes, or errors. Add a
focused check when existing coverage would miss an important regression. Before
editing, record the command, feature flags, input, and expected observable
result. Run it at the starting revision and record any pre-existing failures.
Reuse the same downstream assertion at every checkpoint. Add a separate
assertion when an upstream behavior is supposed to become available.

## Verify each checkpoint

Resolve textual conflicts by reading the base, both sides, and the intent of
their changes. For conflicts in meaning, trace affected callers and run the
smoke checks even when the merge is clean and the code compiles. Pay particular
attention to changed defaults, errors, and wiring that can alter behavior without
changing a public signature. Ask when available evidence leaves an incompatible
behavior choice unresolved.

Run the checkpoint's smoke checks before proceeding. If a check fails, keep the
last verified tip reachable and diagnose the candidate in the task workspace.
Retry when the diagnosis suggests a concrete fix or a better checkpoint boundary.
If progress is blocked, report the failing check and the last verified revision.
Run the affected repository checks against the final candidate, then verify and
report the exact upstream inputs, integration commits, passing checks, and any
remaining gaps. Verify a clean working copy in the task workspace before
handoff. Publish only when authorized.
