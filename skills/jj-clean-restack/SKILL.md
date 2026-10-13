---
license: MIT
name: jj-clean-restack
description: >
  Clean up a messy linear Jujutsu change stack into a separate, reviewable
  stack while preserving the original commits (pinned with a tag), existing
  refs, incremental feature history, and the final tree. Reconstruct from
  commit intent and meaningful intermediate states; duplicate only a small,
  manually confirmed reusable slice. Use when fixups, mixed commits, poor
  ordering, or temporary history need to be reorganized without rewriting the
  existing stack.
---

# Clean A Jujutsu Stack

Build a separate, reviewable stack from the original history's intent and
meaningful intermediate states. Preserve the original graph, existing refs,
and final tree. This skill handles linear stacks; merges, unrelated branches,
generated-artifact policy decisions, or content changes require an explicit plan.
Do not replace the user's branch or publish over it.

## Operating contract

- Original commits and the retained prefix are untouchable. Before every
  mutation, read and apply [scope and safety](references/scope-and-safety.md).
  Never bypass protection with `--ignore-immutable`.
- Create only the safety tag `ORIGINAL_TAG` and dedicated `CLEAN_BOOKMARK`.
  Existing refs and the safety tag never move. A bookmark cannot pin the
  original; a second tag must not track the rebuilt stack. Advance the clean
  bookmark only to a manually validated tip.
- Preserve the final tree unless the user explicitly approves a content change,
  including reformatting preserved content. Preserve meaningful intermediate
  features, migrations, compatibility stages, and removals even when absent at
  the tip; omit a state only with evidence that it is noise or invalid partial work.
- Duplication is limited to a small, explicitly named slice whose complete
  commits were manually inspected and are fully or mostly reusable. Never
  duplicate a range, the whole stack or suffix, or several slices collectively
  reproducing them. Never use `jj rebase` to arrange history.
- Never directly edit an existing duplicate or reconstructed commit, including
  by moving `@` or using `jj edit`. Correct it in a verified child and squash
  only when the whole correction belongs to that owner. Map multi-owner hunks
  and use explicitly scoped absorb or split. Read-only `jj edit` for validation
  remains allowed. Syntax matching and line provenance do not decide ownership.
- Every created or rewritten commit must pass manual parent-diff review,
  dependency checks, and relevant behavior tests before continuing. Tests,
  summaries, and tree equality cannot replace reading the diff. Revalidate all
  rewritten owners and affected descendants oldest first; never accumulate
  unchecked commits or report them as validated.
- Stop on ambiguity, unexpected merges, intersections with original suffix
  commits, unexplained conflicts, or tree mismatches. Use
  [validation and recovery](references/validation-and-recovery.md) when an
  invariant fails.
- Keep full commit IDs/Git hashes internal. In conversation, plans, tables,
  and reports, identify revisions with short jj change IDs (`change_id.short()`)
  and enough description/ref/role context to disambiguate them. Do not paste
  hash-bearing output. Format commands, flags, revsets, and IDs as inline code
  or fenced `sh` blocks.

## Workflow

1. **Freeze scope.** Establish explicit `BASE` and `OLD_TIP`; never infer the
   tip from `@` alone. Inspect the linear graph and record original full commit
   IDs outside the repository when practical. Pin the tip with `ORIGINAL_TAG`
   using `jj tag set` and reserve an unused `CLEAN_BOOKMARK` name. Follow
   [scope and safety](references/scope-and-safety.md).
2. **Plan from history.** Read every original parent diff and milestone tree.
   Use [dependency and conflict analysis](references/dependency-analysis.md)
   to collect advisory evidence for the dependency map.
   Follow [reconstruction tactics](references/reconstruction.md) to present
   the original inventory, complete redistribution map, and ordered clean stack
   before reconstruction. Account for dependencies, meaningful states, and
   validation. Prefer coherent feature slices spanning crates/layers and their
   integration/tests; separate upstream work only when independently ready.
   Retain the longest prefix needing no content, description, or order changes;
   set `REBUILD_BASE` to its tip, or `BASE` when none qualifies. If all commits
   qualify, report that no rebuild is needed.
3. **Build one milestone.** Reconstruct from selected original diffs, milestone
   trees, and explicit edits. Apply a confirmed reusable slice one revision at
   a time at its planned position. Final-state partitioning requires a
   commit-by-commit audit proving no meaningful state is lost; it is not a
   fallback for prohibited duplication. Never restore content also being
   duplicated. Record source milestones, restores, hunk destinations, and mappings.
   For structural overlaps, follow
   [conflict resolution](references/conflict-resolution.md) with the scoped
   Mergiraf profile or guided manual resolution in correction children. If the
   build reveals wrong dependencies, revise the plan rather than reshuffling
   completed commits.
4. **Validate before advancing.** Apply the
   [per-commit protocol](references/validation-and-recovery.md#per-commit-check-protocol)
   to each created or rewritten boundary. Give duplicate/new commits final
   descriptions following the repository convention, without fixup/WIP or
   placeholder wording. Rebuild-produced content must pass the repository's
   formatter and linters. Create `CLEAN_BOOKMARK` after the first validated
   rebuilt commit and advance it only after subsequent gates pass. Repeat
   steps 3–4 for the remaining milestones.
5. **Verify and report.** Record `CLEAN_TIP` and verify the bookmark target,
   final-tree equivalence, preserved semantic timeline, original IDs/refs,
   retained-prefix IDs, and separate suffix. Check conflicts, unexplained
   empties, descriptions, and recorded per-commit evidence. Follow the
   [final validation and report](references/validation-and-recovery.md);
   report skipped checks and remaining caveats rather than claiming validity.
