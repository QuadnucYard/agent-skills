# Selective Feature Extraction

Use when the user requests only part of a stack, including stripping features
from the rebuilt result. The original stack and refs remain preserved. Do not
drop behavior merely because a commit looks unrelated or is difficult to apply.

## Partial porting or a focused full rebuild

Establish which output the user wants; feature picking need not rebuild the
whole source stack. Both modes select semantic changes across commits: each
source commit may contribute focused hunks, shared prerequisites, and unrelated
work. Do not treat commit boundaries as selection boundaries.

- **Partial restack/porting (feature picking):** rebuild only the requested
  capabilities and their available dependency closure. Record other work as
  excluded or deferred, with source ownership and the missing prerequisites
  that would make later porting possible. An unrelated feature whose dependency
  has not been ported does not block the selected result. If a selected change
  needs that dependency, include an authorized prerequisite, use an evidenced
  adaptation, or mark that selected part blocked; never silently omit it or
  expand the selection. Deferred work need not be reconstructed or verified.
  Compare the completed selection to its extraction/integration target, not
  to the full source. This is a completed scoped result, not an interrupted
  attempt to rebuild every feature.
- **Full rebuild with a focused prefix:** account for and rebuild all requested
  source work, placing the features of interest first and the rest in a trailing
  suffix. Keep prerequisites in dependency order. If focused work depends on
  out-of-focus work, move the necessary support into the verified prefix or
  report the ordering conflict; the prefix must work without its suffix.
  Out-of-focus does not mean excluded. If the user explicitly requests only
  its presence, preserve that suffix without requiring design/behavior review,
  per-commit build/tests, or a validated suffix target. Record the waiver and
  exact boundary; otherwise normal whole-stack verification applies.

For presence-only work, retain source-to-result contribution accounting and
source/ref protections. Record known conflicts, missing dependencies, and
unverified behavior without repairing them merely to satisfy waived checks.
Do not claim the complete stack is verified. Reserve later validation at the
first deferred prerequisite/feature boundary, with the evidence still needed.
This trailing-suffix mode differs from behavior-preserving mainline residuals,
which remain on separate branches when that contract is requested.

## Behavior-preserving mainline

When the user requires a behavior-preserving mainline, record the exact behavior
baseline and its contracts; do not assume the full source tip is that baseline.
Keep only behavior-preserving work on the mainline. Treat every feature or fix
that changes the baseline as a residual, whether already in the source or newly
proposed. A useful or authorized fix still changes behavior and does not belong
on this mainline. Repairs to reconstruction mistakes restore the baseline;
they do not authorize repairing baseline defects.

Map residual hunks, integration, tests, and dependencies separately from retained
refactors. When residuals are to be kept, plan separate semantic side branches
and fresh reference bookmarks. For `A -> B -> C`, a residual may branch from
`B` or `C`, according to its prerequisites, without becoming a mainline ancestor.
Do not absorb it into a refactor or merge it back to satisfy source-tip equality.
If retained work needs a residual's behavior, revise the boundary or report the
dependency conflict; do not silently relax behavior preservation.

Use the extraction target protocol below when the source mixes retained work
and residuals. Verify mainline behavior against the recorded baseline, and its
tree against the independently prepared target. Audit every residual's content,
branch point, and preservation destination. Same-base history-only restacks still
preserve the source tree; they do not implicitly request this narrower mainline.

## Define the retained contract

Inventory the whole source before selecting. Record each feature as retained,
excluded, or unresolved, with its entry points, consumers, source hunks, tests,
and shared support. Use `recognize-stack-features` when available; otherwise
establish this evidence directly. Mixed commits require hunk/symbol ownership,
not whole-commit selection. Include later fixes and integration scattered across
the stack, and meaningful intermediate states even when absent from the tip.

Close the retained set over semantic prerequisites. For a retained feature that
depends on an excluded one, retain only demonstrably separable shared support,
plan an authorized adaptation preserving the retained contract, or report the
selection as blocked. Do not silently retain the excluded capability or broaden
the removal. Keep support needed by remaining consumers; remove exclusively
excluded wiring, configuration, exports, tests, documentation, dependencies, and
generated artifacts according to repository policy. Shared tests may need
rewriting rather than deletion. Removing behavior already present at `BASE`
requires explicit scope; omitting a stack addition must not erase base behavior.

Record migration and persisted-data implications. Determine whether removing a
feature requires compatibility handling, cleanup, or retention of a migration.
A feature added and removed within the source still needs an explicit historical
disposition. The retained prefix ends before the first excluded or adapted owner.

## Specify the target before rebuilding

For another destination base, compose extraction into the integration target
described in [the handoff contract](plan-contract.md#another-destination-base).
Prepare it on the destination, preserving destination-provided behavior unless
its removal is explicitly authorized; the same-base child-of-source preparation
below does not apply.

The handoff names the extraction request, retained/excluded feature map,
dependency decisions, authorized adaptations and fixes, and expected full delta
from the source to the retained result. Map every exclusion and adaptation to
source evidence and checks. A path allowlist is insufficient when retained and
excluded behavior share a file. Unresolved selections block affected execution.

Require an independently prepared retained-feature target: after source fixes,
the executor subtracts the planned exclusions and applies planned adaptations on
a separate child line of the corrected full source, validates it, and pins a
fresh immutable target tag. This is a comparison tree, not the clean history.
Do not derive it by copying the rebuilt tip or bless an unexplained delta after
the fact. Exact target identity is execution evidence; its intended content and
acceptance criteria belong in the plan.

The clean tip must equal this target. Review the entire full-source-to-target
delta against the extraction map, and the pre-fix-to-clean delta against fixes
plus extraction. Test retained behavior and relevant interactions, and verify
excluded public entry points or registrations are absent as intended. Passing
tests alone cannot prove no unplanned change occurred.

If excluded features should be delivered later, identify their preserved source
and the retained contracts they depend on; reserve extension seams without
implementing or rebuilding a second stack unless requested. Multiple requested
outputs need separate scopes, targets, mappings, and result refs; equality applies
per output, not between different selections.
