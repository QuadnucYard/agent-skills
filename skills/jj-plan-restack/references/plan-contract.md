# Restack Plan Handoff

The plan describes intended results; an execution record describes observed
results. Keep both tied to the same source snapshot. A plan is not permission
to implement recommended fixes outside the user's authorized scope.

## Required contents

For a different destination base, apply the contract below in addition to these
contents; it replaces same-base source-tree equality and prefix assumptions.

1. **Scope and snapshot.** Repository, explicit base and source tip, linear
   source range, relevant refs and working-copy state. Keep exact commit IDs,
   tree identities, and operation ID in an internal snapshot record; reference
   it from the plan. Use short change IDs plus descriptions in user-facing views.
   Record unsupported graph shapes or policy decisions as blockers.
   For a behavior-preserving mainline, name the exact behavior baseline and
   contracts. Map all behavior-changing features/fixes to residuals, with branch
   points, dependencies, checks, and fresh bookmarks for work kept as reference.
   Include these branches separately from the ordered mainline; use the
   [behavior-preserving contract](feature-extraction.md#behavior-preserving-mainline)
   and extraction target when the source contains residual behavior.
2. **Review and fixes.** Requirements, evidence-backed findings, acceptance
   criteria, authorized behavior changes, recommendations, and unresolved
   decisions. Give each proposed fix a stable label, verification, and clean
   destination. The executor will bind labels to actual verified top commits.
   Label design questions by priority and affected work, with resolution triggers.
   Keep immature optional features outside executable fixes and target commits;
   record only minimal extension possibilities. Essential immature designs require
   an investigation or redesign gate, not speculative implementation. Preserve
   source content unless a correction or exclusion is authorized.
3. **History accounting.** Original inventory, semantic timeline, and complete
   redistribution map from [stack design](stack-design.md). Account for every
   source change, meaningful hunk, and state, including removals absent at the tip.
   Retain each commit's later code fate, consumer status at introduction and tip,
   adopting/refactoring revisions, and development-line labels and definitions;
   carry line membership through the redistribution map to target owners.
   Include the map produced by `recognize-stack-features`, the user's corrections
   and confirmed decisions, and unresolved questions. Pending feature discussion
   or required scope decisions block an executable handoff.
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
   unchanged. Reserve fresh safety-tag, clean-bookmark, and planned residual
   bookmark names; only these new bookmarks may move. With authorized fixes
   intended for the mainline, the clean tree equals the verified corrected
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

## Another destination base

When the user requests rebuilding onto another branch (often a newer trunk),
keep `BASE` as the excluded source base and pin the destination's exact commit
and tree separately as `DESTINATION_BASE`. Record both in the snapshot and
check both for drift. Do not change the source range to the destination range.

Compare source intent with the destination's implementation, consumers, tests,
and relevant history. Classify each source change at hunk/capability granularity
as still needed, fully ported, partially ported, or superseded. Record the
destination evidence and replacement contract, not just matching patch text,
subjects, an empty patch, or a conflict. Skip fully ported or superseded work;
for partially ported work, rebuild only the still-needed remainder and its
integration/tests. Map dependencies to destination-provided contracts or new
owners. Preserve newer fixes and intentional removals; do not resurrect obsolete
implementations or replay already integrated migrations. Uncertain equivalence,
compatibility, or supersession needs investigation or a user decision before
omitting affected work. Reconcile these dispositions in the feature discussion.

Set `REBUILD_BASE=DESTINATION_BASE`. Source commits already in destination
ancestry are base-provided evidence, not a source prefix to replay. Retain a
source prefix only if its exact ancestry already satisfies the requested base;
otherwise its length is zero. Keep the destination immutable under the same
source/ref protections. The requested base change is not a history-only no-op.

The rebuilt tip's identity changes, and its tree generally differs from the old
source tip; source-to-clean tree equality is no longer the completion invariant.
Specify an independently prepared integration target on the pinned destination,
combining the remaining source intent, authorized fixes/extraction, and necessary
adaptations. Require validation and a fresh immutable target tag before clean
reconstruction. Never derive this target from the rebuilt tip. Audit both the
destination-to-target delta and the source-to-target delta, separating inherited
destination changes, ported/superseded work, adaptations, and authorized changes.
Require clean-to-target tree equality plus behavior checks against the actual
destination APIs and contracts. If every change is supplied or superseded,
the verified result may be the destination itself, with complete skip accounting.

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
