# Skill Routing

Every skill named here is shipped in this repository. These are routing
contracts, not bundled dependencies: installing the workflow alone does not
install the other skills. Resolve available copies by name and install only
through an authorized installation task. Select only the rows needed for the
current task, keeping routing within this collection.

## Requirements, design, and delivery

| Situation | Skill | Evidence passed onward |
| --- | --- | --- |
| Establish understanding or compare refined requirements with the original | `requirement-alignment-check` | Confirmed understanding, authoritative obligations, alignment gaps, ambiguity dispositions, acceptance criteria. |
| Design a feature or extension and sequence its implementation | `feature-planning` | Confirmed design decisions, ordered working increments, dependencies, validation, confidence, and extension boundaries. |
| Audit a supplied or newly produced substantive implementation plan | `feature-plan-review` | Readiness judgment, structural repairs, dependency gates, missing acceptance cases, and unresolved decisions. |
| Review implemented code, a PR, or a stack | `code-review` | Conformance and adoption findings, categories, acceptance impact, owners, and focused verification. |
| Audit claims made by a bug-fix commit | `fix-commit-review` | Claim status, root-cause completeness, cost and ownership findings, existing-feature repairs versus corrections to the reviewed commit. |

For a focused requirement or planning request, finish with that artifact and its
open decisions. For a focused review, finish with findings and evidence limits.
For authorized implementation, carry the same requirements through fixes,
review, and verified commits without requesting the same permission again.
The selected skills' explicit confirmation gates still apply; time and silence
cannot satisfy them.

## History and working-copy operations

Choose by the requested result and preservation contract. Do not run these as
an automatic post-implementation checklist.

| Situation | Skill | Boundary |
| --- | --- | --- |
| Understand a stack's actual capabilities and dependencies | `recognize-stack-features` | Read-only evidence for reviews, splits, and restack planning; reuse an existing feature inventory when still valid. |
| Describe or finish ordinary jj work | `jj-commit` | Owns descriptions and ordinary task commits; description-only and message-only requests retain their scope. |
| Split a bounded set of mixed jj changes into semantic units | `jj-split` | Preserve combined behavior and original history as specified; splitting grants no behavior-fix authority. |
| Review a jj stack and design a broader reconstruction | `jj-plan-restack` | Owns read-only review, source snapshot, semantic timeline, redistribution, boundaries, and handoff. |
| Reconstruct a jj stack from an actionable plan | `jj-execute-restack` | Owns authorized fixes, source protection, separate reconstruction, milestone checks, final-tree proof, and recovery. |
| Layer fixes while preserving original target IDs | `jj-patch-stack` | Additive patches; applying their squash guide needs explicit rewrite authorization. |
| Diagnose missing objects or damaged jj operation/working-copy metadata | `jj-repair-state` | Read-only diagnosis first; its recovery procedure supersedes ordinary snapshotting or cleanup commands while state is broken. |

An execution request without an actionable restack plan starts with the planner
and continues to the executor within existing authorization. Planning itself
adds no approval gate. With a valid supplied plan, enter the executor directly;
do not replan by default. Changed source identities or unresolved decisions
return affected work to planning.

Feature recognition is shared analysis, not a second competing plan. Pass its
inventory to the owning review or history workflow. A straightforward local
split does not require a full reconstruction. Preserve a patch-only request's
additive guarantees instead of substituting a restack.

For ordinary jj task boundaries use `jj-commit`. During a specialized history
operation, its owner also owns conflict handling, mutation restrictions, and
recovery. Use the target repository's language and testing conventions directly
when implementing changes; this collection's workflow adds no separate language
skill dependency.

## Experimental and research work

| Situation | Skill | Boundary |
| --- | --- | --- |
| Design a benchmark, audit an experiment, or investigate anomalous results | `experiment-design-and-audit` | Establish claims, fair comparisons, execution validity, and evidence limits before using results to justify behavior or performance changes. |
| Rigorously critique a design, specification, argument, or explanation | `seminar-supervisor` | Add when requested or when substantive reasoning needs this lens; reuse domain-review findings rather than duplicating the review. |
| Rehearse or review a research meeting update | `weekly-research-mentor` | Route only for the research communication task; meeting critique is not an implementation prerequisite. |

A performance repair can combine the experiment skill for measurement validity
with the fix-review skill for the code repair. Each owns a distinct question;
neither one's verdict establishes the other's conclusion.
