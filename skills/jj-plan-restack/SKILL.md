---
license: MIT
name: jj-plan-restack
description: >
  Review a Jujutsu stack's behavior and design adoption, then plan coherent
  commit boundaries, dependencies, fixes, and validation. Use for restack
  planning or review without changing source files, history, refs, or configuration.
---

# Plan a Jujutsu Restack

Produce an actionable reconstruction plan. Review the whole stack before
choosing boundaries. This skill works independently of `jj-execute-restack`.

## Review and design

- Require the intended repository's `.jj` directory and verify `jj root`.
  Resolve explicit `BASE` and `SOURCE_TIP`; never infer the stack from `@` alone.
  Use `jj --no-pager --ignore-working-copy` and a fixed operation for source
  reads. Preserve files, history, refs, working-copy state, and configuration;
  write only requested planning artifacts and temporary analysis files.
- Find the requirements in the request or supplied specification. Read every
  source change's full description (subject, body, and trailers), every parent
  diff, relevant milestone tree, final implementation, callers, and tests.
  Use `jj --no-pager --ignore-working-copy --at-op <op> log --no-graph -r <source> -T description`
  for full descriptions at the fixed snapshot; read any truncated output in
  full before choosing boundaries. Subjects and shortened log views do not
  replace this reading. Preserve substantive description details in the plan
  and proposed descriptions; follow the stack-design accounting rules below.
  Review design adoption, observable behavior, errors, compatibility, lifecycle,
  and interactions. Mark unavailable requirements or evidence as unverified.
  Do not spend review time on formatting or linter checks.
- Follow [stack design](references/stack-design.md) for the inventory, semantic
  timeline, redistribution map, boundaries, and order. Use the read-only
  [analysis helpers](references/dependency-analysis.md) for advisory evidence;
  textual applicability does not establish semantic dependency or ownership.
- Propose fixes with acceptance criteria and destination owners; do not implement
  or commit them. Distinguish authorized fixes from recommendations and unresolved
  behavior decisions. A history-only request preserves the source tree.
- Cover the full design and reserve justified future extension boundaries without
  speculative implementations. Preserve meaningful migrations and removals,
  including capabilities absent from the final tree.

## Deliver the plan

Use the [handoff contract](references/plan-contract.md). Retain the longest
unchanged prefix; a later fix targeting it moves the affected boundary into the
rebuilt suffix. If no changes are needed, report a no-op.

Use short jj change IDs with descriptions in user-facing material; keep exact
commit and operation identities in a separate internal snapshot record. Local
plan files are deliberately untracked: do not check their tracking status or
reread them merely to confirm they were written.

For an execution request, continue with `jj-execute-restack` after planning when
available and authorized. Planning creates no new approval requirement. If the
executor is unavailable, deliver the plan and report that execution needs it.
