---
license: MIT
name: jj-review-restack
description: >
  Review a Jujutsu change stack for design adoption and behavior, commit needed
  fixes on top, then rebuild it with jj-clean-restack. Use when the desired
  history puts confident changes early and removes intermediate rewrites while
  preserving the original stack and verifying the corrected final tree.
---

# Review and Rebuild a Jujutsu Stack

Produce a dependency-correct, reviewable stack whose early changes are the most
confident independent units and whose commits express the final design. Review
the whole stack before choosing its boundaries or order.

Use the bundled [jj-clean-restack guidance](references/restack/overview.md) for reconstruction. Read it and its applicable references before mutation. The bundle makes this skill usable when installed alone; the repository maintains it from the canonical `jj-clean-restack` skill. Do not substitute an in-place rebase for the requested reconstruction.

For local jj operations, inspect the repository boundary first: require a `.jj` directory for this workflow, and verify that `jj root` identifies the intended repository rather than a parent. Use `jj --no-pager` for output and noninteractive commands with explicit descriptions; avoid editor or TUI commands. In a colocated repository use jj for mutations and Git only for read-only verification. Preserve unrelated work and record the operation ID before mutation. Follow an installed `jujutsu-workflow` skill when available, subject to this skill’s stricter preservation rules.

## Establish scope and review

- Resolve the repository, base, and intended tip from the request and graph;
  do not assume the working-copy revision alone identifies the stack. Record
  full commit IDs, current refs, working-copy state, and operation ID. Protect
  unrelated work and preserve original revisions. Clarify only genuinely
  ambiguous scope or unsupported graph shapes such as merges.
- Read every diff and the final affected code, including callers, tests, and
  integration points. Subjects are clues, not evidence of intent or dependency.
- Focus on design adoption and observable behavior: whether new abstractions
  are actually used, callers migrate coherently, invariants hold, and obsolete
  paths disappear. Check relevant error handling, compatibility, persistence,
  lifecycle, and feature interactions. Do not spend review time on formatting
  or linter checks.
- Consider the complete design and reserve relevant future extension points
  without inventing speculative implementations. Identify decisions that must
  be made now rather than deferring known gaps. Do not label plans with `V1`.

## Fix before reconstruction

If review reveals a defect, make the fix in a new change on top of the original
stack, with a meaningful description and focused behavioral verification.
Never hide a fix inside restack conflict resolution or edit an original commit.
Keep fixes distinct from unrelated working-copy edits. Seek clarification when
the correct behavior requires a material product or design decision.

Pin the pre-fix tip, then record and pin the corrected tip after all fix commits
are complete, using fresh tags under the restack skill's safety rules. Inspect
the pre-fix-to-corrected diff so each intentional behavior change is explicit.
If no fixes are needed, these two tips are the same. Use the corrected tip as
`OLD_TIP` and the equivalence target for reconstruction. Preserve the pre-fix
tip separately so the original behavior and the fixes remain comparable.

The user's request to fix defects authorizes those top commits; tree
preservation during reconstruction applies to the corrected tip. Any new defect
discovered while rebuilding must first receive an explicit top fix on the
preserved source stack, followed by an updated pinned target and build plan.

## Choose boundaries and order

Build a compact source-to-intent map containing dependencies, confidence and
its evidence, review findings, and proposed disposition: keep, squash, split, or
replace with a commit reconstructed from the final state.

1. Respect semantic dependencies first. A commit must work with its ancestors,
   without depending on later repairs or migrations.
2. Among independent units, put the most confident, well-understood changes
   first. Use demonstrated correctness and adoption, not size or clean patch
   application alone. Keep uncertain decisions later when dependencies allow.
3. Eliminate transitional implementations and repeated edits. Fold fixups
   into their final intent, remove net-zero churn, and separate mixed purposes
   where doing so produces coherent behavior at each boundary.
   Explicitly consider squashing related changes that together implement one
   coherent purpose, including an implementation and its follow-up corrections,
   adoption, or tests when separate commits would be incomplete or misleading.
   Squash their rebuilt counterparts into the appropriate logical owner using
   `jj-clean-restack`; keep the original revisions untouched. Do not squash
   merely because changes touch the same files: preserve independently useful
   changes and required migration boundaries. Record which source changes are
   combined and why the resulting commit is independently valid.
4. Move stable structural preparation ahead of features that would otherwise
   be rewritten by it. For example, if source change A adds a field and B
   refactors the containing struct, place B's independent structural work
   first and add A's field directly to that final structure. If B depends on A,
   split out the independent preparation or rebuild their final intent together;
   do not mechanically reverse them into a broken sequence.
5. Avoid add-then-move history. If an item is first added to module/file A
   and later moved to B, introduce it directly in B in the clean stack.
   Include the required wiring and callers at that boundary. Retain an
   intermediate location only when a real compatibility or migration
   requirement needs it.
6. Preserve meaningful migration stages when compatibility or rollout requires
   them. Removing intermediate rewrites must not remove necessary behavior.

Explain why the proposed order works and how every original intent and fix is
represented. A local plan file is deliberately untracked: do not check its VCS
tracking status or repeatedly reread it merely to confirm it exists.

## Rebuild and verify

Execute with `jj-clean-restack`: retain the original graph and existing refs,
retain the longest unchanged prefix and grow a separate suffix from the
first divergence point, then choose duplicate-in-final-order or final-state
reconstruction according to the dependency analysis. Follow its rules for
amending created commits through verified child fixes, pinning tips, and
recovery. Do not reorder finished duplicates through rebase.

Verify exact tree equivalence between the clean tip and the corrected source
tip. Also inspect the pre-fix-to-clean diff: it must contain precisely the
reviewed fixes. Confirm original commit reachability, unchanged existing refs,
graph separation, and absence of unexplained conflicts or empty commits.

Verify meaningful intermediate behavior with focused tests or build checks
appropriate to the changes. Inspect design adoption at each relevant boundary.
Honor mandatory repository checks and reconstruction-specific checks from
`jj-clean-restack`, but do not broaden the review into a formatting/lint audit.
Distinguish tests actually run from conclusions based on inspection.

Report findings and top fixes, the final ordered commits with reasons and
source mapping, preserved and clean tip identifiers/tags, tree-comparison
evidence, and any verification limits. Do not publish or move the user's
existing branch as an implicit consequence of rebuilding.
