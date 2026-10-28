# Selective Feature Extraction

Use when the user requests only part of a stack, including stripping features
from the rebuilt result. The original stack and refs remain preserved. Do not
drop behavior merely because a commit looks unrelated or is difficult to apply.

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
