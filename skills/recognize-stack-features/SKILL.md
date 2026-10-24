---
name: recognize-stack-features
description: >
  Infer vertical features and their dependencies from actual changes across a
  commit stack, regardless of original commit boundaries. Use for feature
  inventories, stack reviews, splitting, and restack planning, including as a
  shared analysis step referenced by other skills.
license: MIT
---

# Recognize Stack Features

Recover the capabilities a stack actually delivers and the changes each needs.
Produce an evidence-backed feature map for a calling workflow. Recognition alone
does not authorize code edits, history changes, or implementation of missing work.

## What counts as a feature

A feature is a coherent, independently meaningful capability delivered vertically
through the necessary layers: implementation, integration, and actual downstream
use, with the proven-independence exception below for complete standalone
contracts. It can add behavior, repair existing behavior, or change how an existing
production path works. Vertical does not require touching every architectural
layer; it requires completing the path relevant to the claimed outcome.

- **Require a real consumer.** Trace a changed producer, API, representation, or
  mechanism to downstream production code and an observable result. The consumer
  may already exist at the base; show how the change reaches it. Tests, mocks,
  benchmarks, examples, exports, and declarations alone do not establish adoption.
  A consumer is downstream in the execution or dependency path; it need not be in
  a later commit or another package.
- **Allow proven independence.** A change can stand alone if it delivers a useful
  contract without later in-stack adoption, such as a supported library API for
  external consumers, a complete CLI operation, or a refactor of an already used
  path. State the contract, intended consumer or existing entry point, and why
  later changes can be removed without losing its purpose. A public keyword,
  passing unit tests, or hypothetical future reuse is insufficient evidence.
- **Do not promote preparation to a feature.** If an addition has no real
  consumer and no demonstrated independent purpose, attach it to the feature
  that first needs it. If no such feature exists in scope, report unused,
  incomplete, or unverified work. Never invent a consumer to complete the map.
- **Separate verification from delivery.** Tests validate an identified contract;
  they cannot supply its missing production consumer. Associate test-only work
  with the behavior it verifies, or report it as independent verification work
  without claiming a new production feature.

## Establish the evidence

Resolve an explicit excluded base, included tip, and source graph. Pin immutable
revision identities before reading; include relevant ancestors and merge parents.
For nonadjacent selections, identify intervening changes and prerequisites outside
scope rather than silently treating the selection as a contiguous stack.

Read every parent diff, the base-to-tip result, relevant intermediate trees, and
the surrounding implementations and callers. Commit messages and existing slices
are search hints only: both may describe bad grouping. Infer what changed from
code and actual use; supplied requirements establish intended outcomes, while
inferred intent remains provisional. Do not spend recognition time on formatting
or linter checks.

For repeatable evidence collection in Git or colocated jj repositories, use the
bundled Python 3.11+ helper with Git supporting `--attr-source`, from this skill's
installed directory:

```sh
python scripts/stack_evidence.py --repo REPOSITORY --base BASE --tip TIP --output NEW_DIRECTORY
```

Add repeated `--term IDENTIFIER` arguments to find literal candidate references
in the base and every selected tree. For jj, resolve revisions to Git commit IDs
using read-only `jj --no-pager --ignore-working-copy` commands at a fixed operation
first. The script accepts Git revisions, not jj change IDs; it never snapshots jj
or reads uncommitted source files. Inherited Git repository selectors are ignored;
attributes come from the inspected revision instead of the working tree.
For a backend without Git access, collect equivalent
evidence with the repository's native read commands.

The helper writes `manifest.json`, `net.patch`, and per-revision tree indexes,
per-parent patches, and optional candidate matches. Merge parents remain separate;
parents outside the selected range are identified as context. Use the pinned IDs
to read full source with `git show COMMIT:path`. The script does not recognize
features or classify consumers. Matches include tests and dead code; absence of a
literal match cannot exclude indirect calls, registration, generated code, or
external consumers. Binary blobs and submodule contents need separate inspection.
Only use a successful run with a complete manifest; failures leave partial output.

## Infer boundaries from behavior

1. **Describe actual outcomes.** For each changed behavior, name its entry point,
   before/after contract, producer, downstream consumer, and effect. Trace data,
   control flow, registration, configuration, and relevant failure paths. Inspect
   existing callers as well as changed ones. Enumerate distinct production effects
   before grouping their code. Mark broken or missing wiring.
2. **Build a many-to-many source map.** Assign meaningful hunks, symbols, wiring,
   removals, and coverage to candidate outcomes. One commit may contain multiple
   features; one feature may span several commits, including early commits with
   no consumers. Neither shared files nor separate commits settle ownership.
3. **Close each vertical path.** Combine implementation with the downstream
   adoption needed for its outcome. Follow later corrections, moves, and renames
   to their semantic owner. A correction to a feature introduced within the stack
   belongs to that feature; a fix to preexisting behavior may be independent.
   Record when the outcome first works and any later revision to its contract.
4. **Challenge separation and merging.** Ask whether removing the other candidate
   leaves a useful, complete capability on its declared prerequisites. Split when
   both capabilities have distinct outcomes and valid paths; combine when the
   proposed units only provide horizontal fragments of the same outcome. A
   dependency between two complete capabilities does not make them one feature.
   A later optional capability is its own candidate when the earlier behavior
   already works and the extension has a distinct usable contract. Do not absorb
   it just because it extends the same path. Co-location in a commit is never
   evidence that an unrelated production effect supports another feature; require
   a demonstrated causal or contract dependency for that ownership.
5. **Resolve shared support explicitly.** A helper serving several features is
   not automatically a standalone feature. Give its necessary introduction to a
   complete first adopter, with later adopters depending on that contract, unless
   independence is demonstrated. Record shared ownership and incremental changes
   without counting the same implementation twice. Do not merge all consumers
   simply because they share a helper or form a connected dependency graph.
6. **Reconcile the timeline and scope.** Preserve meaningful migrations, removals,
   compatibility stages, and capabilities introduced then removed before the tip.
   Distinguish durable outcomes from abandoned scaffolding or rewrites. A net
   diff alone cannot make this distinction. Include merge-resolution behavior;
   do not attribute it automatically to either branch.

Apply the same reasoning to internal refactors and maintenance: show the existing
production behavior they preserve or repair. Keep genuinely independent support,
verification, documentation, and noise visible without forcing every source hunk
to be a new feature. Uncertainty is a reported gap, not evidence of independence.

## Hand off a reusable feature map

Use stable feature labels independent of source commit numbers. Scale the detail
to the stack, but retain these facts for each candidate:

- **Outcome and status:** the concrete contract and whether it is delivered,
  incomplete, removed later, or unverified; classify independent nonfeature work.
- **Vertical evidence:** entry point → changed mechanism → downstream production
  consumer → effect, with revision and source locations. For independence,
  provide the explicit justification instead of a fabricated downstream caller.
- **Source ownership:** source commits and relevant hunks or symbols, including
  scattered adoption and fixes; show where a mixed commit splits among features.
- **Dependencies and milestones:** base-provided contracts, other feature labels,
  shared support owners, and the state where adoption becomes complete. Distinguish
  semantic dependencies from chronological order or textual overlap.
- **Validation and gaps:** checks supporting the contract, inspection versus
  execution, missing consumers, unresolved intent, and confidence with reasons.

Reconcile all meaningful source changes with this map, including nonfeature work
and omissions with reasons. Explain where inferred boundaries disagree with the
original slices. Reserve justified extension seams by naming the existing owner
and contract that future work would extend; future consumers do not establish
present adoption or complete an unfinished feature.

Keep feature recognition separate from commit scheduling: a feature can have
meaningful incremental milestones, and shared prerequisites need explicit order.
The calling review, split, or restack skill decides target commits, fixes, and
mutations within its own authorization. Other skills can invoke this skill by
name and consume this map; this skill requires no companion skill.

## Boundary examples

| Actual changes | Recognition |
| --- | --- |
| One commit adds CSV export and repairs login expiry. | Two outcomes with their own production paths; split the mixed source ownership. |
| Early commits add an encoder and tests; a later commit wires it into export. | One export feature spanning the commits; encoder tests are not its consumer. |
| A helper changes; unchanged production callers already reach it. | Adoption can be complete without editing a caller; trace the changed effect through those callers. |
| A complete export path is followed by optional compression and its wiring. | Two vertical capabilities if export works without compression; compression depends on export. |
| Export and upload share a new encoder. | Distinct outcomes can share support; assign its introduction to a complete adopter or justify independent value. |
| A new API has only tests and an unused export. | Incomplete or unused support unless an independently useful external contract is established. |
| A migration enables a real compatibility path and a later commit removes it. | Preserve the meaningful intermediate outcome even if the tip no longer contains it. |
