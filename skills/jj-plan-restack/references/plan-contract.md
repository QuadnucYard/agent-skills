# Restack Plan Handoff

The plan describes intended results; an execution record describes observed
results. Keep both tied to the same source snapshot. A plan is not permission
to implement recommended fixes outside the user's authorized scope.

## Required contents

1. **Scope and snapshot.** Repository, explicit base and source tip, linear
   source range, relevant refs and working-copy state. Keep exact commit IDs,
   tree identities, and operation ID in an internal snapshot record; reference
   it from the plan. Use short change IDs plus descriptions in user-facing views.
   Record unsupported graph shapes or policy decisions as blockers.
2. **Review and fixes.** Requirements, evidence-backed findings, acceptance
   criteria, authorized behavior changes, recommendations, and unresolved
   decisions. Give each proposed fix a stable label, verification, and clean
   destination. The executor will bind labels to actual verified top commits.
3. **History accounting.** Original inventory, semantic timeline, and complete
   redistribution map from [stack design](stack-design.md). Account for every
   source change, meaningful hunk, and state, including removals absent at the tip.
4. **Target sequence.** Longest unchanged prefix and `REBUILD_BASE`; ordered clean
   commit labels, final descriptions, purposes, sources, dependencies, intended
   intermediate behavior, and validation. Include complete proposed subjects,
   bodies, and applicable trailers, preserving substantive source-description
   details with their owners and explaining substantive omissions as required
   by stack design. State source tactics and evidence:
   selective reconstruction, a small confirmed duplicate slice, or a justified
   final-state partition. Reserve relevant extension boundaries, not speculative
   commits. If the whole source qualifies unchanged, state the no-op.
5. **Preservation and completion.** Existing refs and original revisions remain
   unchanged. Reserve fresh safety-tag and clean-bookmark names; only the latter
   may move. With authorized fixes, the clean tree equals the verified corrected
   source and its delta from the pre-fix source is exactly those fixes. Otherwise
   it equals the original source. For [feature extraction](feature-extraction.md),
   include the retained/excluded map, dependency closure, authorized adaptations,
   and complete expected source-to-target delta. Require an independently prepared,
   validated target pinned before reconstruction; clean-to-target equality replaces
   clean-to-full-source equality. Specify checks at every boundary and final
   graph, source, tree, and semantic-timeline checks, plus unavailable evidence.
6. **Result review.** Identify the comparison mode and evidence needed for the
   [post-restack audit](review-restack.md), including exact execution targets,
   source preservation, retained behavior, excluded entry points, and checks at
   intermediate revisions. Execution evidence does not replace this review.

## Execution and changes

The executor checks snapshot identity and plan completeness before mutation,
then records actual fixes, reconstruction identities, and validation separately.
It may choose commands and resolve evidenced mechanical overlaps within the
plan. A changed purpose, dependency, intended behavior, or uncertain ownership
requires revising the affected plan before more reconstruction.

Never move safety tags to update a target. A newly authorized fix gets a new
verified source commit, fresh target tag, updated mapping, and revalidation from
the first affected boundary. Preserve earlier source and execution records.
When resuming, compare protected source state to the original snapshot and
workflow-owned refs and working-copy state to the execution checkpoint. Recorded
fixes and bookmark advances are expected progress. Reuse evidence for unchanged
revisions and parents with still-applicable checks. For description-only
rewrites, require proof of unchanged content and parent trees and an explicit
old-to-new identity mapping; review metadata and graph, and rerun any checks
sensitive to revision metadata or changed execution conditions. Unrelated
operation-log changes alone do not require discarding the plan.

Future merge-aware planning or language-specific analysis can extend source
evidence and graph constraints. Preserve the snapshot, intent mapping, and
validation handoff; unresolved merge semantics block execution today.
