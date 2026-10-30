---
name: jj-split
description: >
  Split one or more Jujutsu commits into semantic commits, putting fixes and
  refactors of existing features first. Follow a restack plan when available.
license: MIT
---

# Split Jujutsu Changes

Split selected changes into **independently valid semantic commits**, preserving
the combined final tree. Splitting does not authorize additional behavior fixes.
Selecting only some resulting features is a restack extraction, not a split
with tree equality waived. Use `jj-plan-restack` and `jj-execute-restack` when
available, or an equivalent explicit selection/dependency plan and independently
validated retained-feature target. Preserve the split-only contract here.

## Choose boundaries

- **Use the plan.** Refer to an available `jj-plan-restack` or equivalent plan;
  verify its source snapshot and honor its boundaries and constraints. Otherwise
  inspect the selected parent diffs and meaningful intermediate states, then map
  every concern to an ordered destination. Use the planner for broader design
  questions when installed; a clear local split needs no full restack plan.
- **Existing features first.** Order existing-feature fixes, preparatory
  refactors, then new behavior. Dependencies take precedence: a refactor needed
  by a fix comes first; a fix to newly introduced behavior belongs with that
  behavior. Keep implementation, integration, and tests together by purpose.
- **Separate broad mechanical refactors.** When a change touches many files and
  a large portion contain only small, repetitive refactors (for example, an API
  migration), extract that refactor into a separate semantic commit so reviewers
  can assess the substantive changes independently. Include the supporting API
  changes and tests needed to keep the refactor valid; order it by dependency.
  Split hunks in mixed-purpose files rather than moving unrelated behavior with
  the mechanical edits. Preserve independently valid commits and the final tree.
- **Account for the whole change.** Include removals, compatibility stages, and
  meaningful states absent from the final tree. Reserve justified future
  extension boundaries without speculative implementation. Treat nonadjacent
  selections as separate groups unless intervening commits are in scope;
  resolve merge semantics before flattening a graph.

Local plan files are deliberately untracked: do not check their tracking status
or reread them merely to confirm a write.

## Split

1. **Protect the source.** Verify `jj root`, explicit base/tip, and working-copy
   state. Record exact source IDs, refs, and the operation; pin the source with a
   fresh safety tag. Preserve unrelated edits, using a separate workspace if
   needed. Build a separate result line; keep original commits and refs intact
   unless replacement was explicitly requested.
2. **Choose per milestone.** Follow the [command recipes](references/recipes.md):
   - **Paths already final:** restore from the final state only when those paths
     reach that state here and have **no later changes**.
   - **Small early commits:** manually build them, then restore the final state
     for the last planned residual.
   - **Large early commits:** duplicate the bounded source unit, subtract, invert
     to extract the early part, then invert and squash to obtain the residual.
   Preserve intermediate milestones when a final snapshot would erase them.
3. **Operate explicitly.** Use noninteractive `jj --no-pager` commands, explicit
   revisions, and complete messages. Check installed help for flags. Mutate only
   workflow-owned revisions through jj; honor a restack plan's duplication
   limits. Temporary subtraction/inverse changes must not survive in the result.

## Verify and finish

- **Each boundary:** read the complete parent diff, check semantic ownership and
  dependencies, and run relevant behavior checks. Recheck affected descendants
  after rewrites. No broken commit may rely on a later repair. Review behavior
  and design adoption, not formatting or linter output.
- **Final result:** require no conflicts and an empty
  `jj diff --from SOURCE_TIP --to RESULT_TIP --summary`; verify source preservation
  and complete source-to-result mapping. Tree equality alone does not validate
  intermediate behavior. Track any separately authorized content fixes explicitly.
- **Descriptions and handoff:** redescribe every result by its actual purpose
  and motivation, especially the residual. Advance only a fresh result bookmark
  after validation. Report ordered change IDs, mapping, safety tag/bookmark, and
  checks or limits; leave a clean working copy. Keep the last validated milestone
  on failure and inspect intervening operations before recovery. Publish only
  when requested.
