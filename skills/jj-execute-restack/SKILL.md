---
license: MIT
name: jj-execute-restack
description: >
  Execute a supplied Jujutsu restack plan, implementing authorized fixes and
  rebuilding a separate verified stack while preserving source history and
  existing refs. Use when an actionable plan is ready for reconstruction.
---

# Execute a Jujutsu Restack

Own mutations and execution evidence. Consume a plan from `jj-plan-restack` or
an equivalent supplied plan; the planner need not be installed. If no actionable
plan exists, use the planner when available rather than inventing boundaries
during execution. Do not publish or replace the user's branch implicitly.

## Admit the plan

- Verify the intended `.jj` repository with `jj root`; use noninteractive
  `jj --no-pager` commands with explicit descriptions. In colocated repositories,
  mutate with jj and use Git only for read-only verification. Preserve unrelated
  work and record the operation before mutation.
- Require a source snapshot record, explicit base/tip and retained prefix,
  original inventory and semantic timeline, complete redistribution map,
  ordered target commits, authorized fixes, per-boundary checks, final-tree
  target, and unresolved decisions. Missing decisions block affected work.
- Compare exact source commit identities, trees, relevant refs, and working-copy
  state to the plan. Short change IDs alone cannot detect rewritten versions.
  Drift blocks affected mutations until an updated plan is available; use the
  planner if installed, otherwise report the evidence and request an updated
  plan. Unrelated operation-log advancement alone does not invalidate a plan.
  Do not change intended behavior or boundaries silently.
- Read [scope and safety](references/scope-and-safety.md) before mutations.
  Preserve original commits and the retained prefix. Never bypass immutability,
  arrange history with `jj rebase`, or duplicate the whole stack or suffix.
  Correct completed rebuilt commits through verified children, never direct
  edits. Scope squash/absorb to their mapped owners; revision checkouts for
  validation remain allowed without modifying those commits.

## Fix, reconstruct, verify

1. **Protect and fix.** Pin the pre-fix source with a fresh tag. Implement only
   planned, authorized fixes as verified new top commits; never edit originals.
   Record their source mapping and inspect the complete intentional delta.
   Pin the corrected source with a fresh immutable tag when fixes exist; it is
   now `OLD_TIP` and the equivalence target. Without fixes, reuse the source tag.
2. **Build one milestone.** Follow [reconstruction](references/reconstruction.md)
   from the recorded `REBUILD_BASE`. Use original diffs and milestone trees,
   duplication only for a small manually confirmed reusable slice, and final-state
   partitioning only with the plan's semantic audit. Do not apply content twice.
   Record actual source-to-new mappings and final descriptions.
3. **Validate before advancing.** Read each complete parent diff and follow the
   [per-commit protocol](references/validation-and-recovery.md#per-commit-check-protocol).
   No broken intermediate commit may depend on a later repair. Advance only the
   dedicated clean bookmark after validation. For structural conflicts use
   [correction children](references/conflict-resolution.md); revalidate rewritten
   owners and affected descendants oldest first.
4. **Finish.** Prove clean-tip tree equality with the corrected source, and that
   the pre-fix-to-clean delta contains precisely the authorized fixes. Verify
   preserved source IDs/refs, retained-prefix identity, separate suffix, semantic
   milestones, and per-commit evidence. Apply the
   [completion and recovery rules](references/validation-and-recovery.md).

## Deviations and reporting

Repair reconstruction mistakes within the existing plan through verified
correction children. New source defects, changed dependencies, ambiguous
ownership, or different commit purposes return to planning. Do not smuggle
behavior changes into conflict resolution. If replanning adds an authorized
source fix, append it to the preserved source, pin a fresh corrected target,
and rebuild from the first affected boundary; never move an existing safety tag.

Keep execution progress separate from intended design: record exact validated
revisions, checks, outcomes, last validated milestone, and pending corrections.
On resume, compare source identities and protected refs to the original snapshot,
and workflow-owned refs and working-copy state to the execution checkpoint.
Recorded fixes and bookmark advances are expected progress, not external drift.
Rewritten trees or parents invalidate affected evidence. A no-op needs no clean
bookmark.

Report findings addressed, final order and source mapping, safety tags, clean
bookmark, tree comparisons, and verification limits. Use short jj change IDs
with role/description context; keep commit hashes in internal records.
