# Stack Design

## Inventory and semantic timeline

Read every source change's full description, parent diff, and milestone tree,
oldest first, including changes proposed for the retained prefix. Read bodies
and trailers without truncation; subjects alone lose intent and rationale.
Descriptions are evidence of stated intent, not proof of behavior or dependency;
check their claims against the implementation. Use the
[analysis helpers](dependency-analysis.md) for advisory lineage and conflict data.

Do not strip substantive details to shorten descriptions. Carry still-valid
behavior, rationale, design decisions, constraints, tradeoffs, compatibility
notes, and relevant provenance or required trailers into the owning target
descriptions. Splitting or combining changes redistributes those details with
their semantic owners. Consolidate repetition and correct stale claims only
with evidence; record why any substantive detail is superseded, unsupported,
or intentionally omitted. Do not silently replace a detailed body with a
subject-only summary.

Classify source changes as coherent intent, incremental feature, migration,
removal, exact or distributed fixup, mixed purpose, dependency correction, noise,
or description cleanup. For each state, identify what becomes true, whether later
changes revise or erase it, why it is meaningful or disposable, and where its
behavior will be represented and validated in the clean stack.

Present all three views; a final-tree partition cannot replace history analysis:

1. **Original inventory.** Every source commit, including the retained prefix:
   short change ID, description, behavior/state introduced or removed,
   dependencies, and later revisions of that state.
2. **Redistribution map.** Every source change, meaningful hunk, and state:
   destination label(s), disposition (retain, reconstruct, duplicate, split,
   squash, absorb, reorder, or omit), and evidence-backed reason. Enumerate all
   owners for distributed fixups. Explain omissions as noise, invalid partial
   work, or explicitly scoped feature exclusions rather than silently dropping
   a reviewable milestone. In extraction, map excluded hunks and dependency
   adaptations as fully as retained work; follow [extraction scope](feature-extraction.md).
3. **Target sequence.** Entire clean stack including the retained prefix:
   ordered label, final description, purpose, source changes/hunks, parent and
   semantic dependencies, intended state, and behavioral validation. Show where
   justified future extensions attach without inventing speculative commits.

Map proposed fixes by stable labels before execution creates their top commits.
Separate recommendations or unresolved behavior choices from authorized fixes.
Do not mark a plan executable while required sources, destinations, dependencies,
states, behavior decisions, or validation remain unaccounted for. If execution
disproves an assumption, revise and re-present affected scope before continuing.

## Coherent slices

Prefer one capability across layers or crates, including its integration,
callers, tests, and documentation. File boundaries and convenient patch
application do not establish independently valid commits. For an upstream API
used by downstream behavior, keep the feature coherent across both unless the
upstream change is independently useful and confidently ready earlier. Record
that evidence; dependency alone does not justify grouping every upstream change
ahead of all consumers.

Map late fixup hunks to their semantic owners, including corrections across
moved or extracted code. Line provenance does not decide ownership. Preserve
meaningful introduction and removal states even when both vanish at the tip.

## Boundaries and order

Respect semantic dependencies first. Among independent units, put the most
confident, well-understood changes first, using demonstrated correctness and
adoption rather than size or clean patch application.

- Fold implementation, corrections, adoption, and tests into a coherent owner
  when separate commits would be incomplete or misleading. Keep independently
  useful changes and required migration boundaries distinct; shared files alone
  do not justify squashing.
- Keep risky performance changes separate; do not squash or absorb them into
  earlier commits. Trivial, low-risk optimizations and clear fixes for evident
  performance problems, such as accidentally excessive algorithmic complexity,
  may be absorbed into their semantic owners when correctness and benefit are
  clear. Otherwise, split optimization hunks from mixed fixes or refactors so
  the preceding commits remain independently valid. When correctness or
  performance benefit is uncertain, put the optimizations in a final suffix
  ordered by dependency. If other changes depend on them, expose that dependency
  and revise the boundaries rather than silently folding the optimization
  earlier. Record the affected workload, comparison baseline, and outstanding
  checks for later verification. Deferral does not waive required correctness
  checks; distinguish evident complexity improvements from measured speedups,
  and mark unmeasured speedup claims unverified.
- Move independent structural preparation ahead of features that would otherwise
  be rewritten by it. If preparation depends on the feature, extract the
  independent part or plan their final intent together.
- Add code at its final location with wiring and callers. If code was added in
  one place and moved later, including within the same file, place it at the
  final location in the introducing commit. Keep an intermediate location only
  when a required migration or compatibility stage needs it.
- Treat blank-line-only changes, including a single added or removed blank line,
  as restack artifacts. Include necessary blank lines in the relevant
  implementation change and omit unrelated edits.
- Preserve meaningful migration, compatibility, and removal stages. Net-zero
  content does not prove that intermediate behavior is disposable.
- Retain the longest initial prefix whose content, descriptions, and order fit
  the plan. A later correction targeting a prefix owner moves that owner and
  subsequent changes into the rebuilt suffix. Never retain scattered originals
  after divergence.

Choose sources per milestone. Prefer original diffs, meaningful trees, and
explicit reconstruction. Duplication is only for a named small minority of
manually inspected, mostly reusable commits, never the whole range or suffix.
A final-state partition requires a commit-by-commit audit proving it loses no
meaningful intermediate state. Plan their sequencing so no content is applied
both by restoration and duplication. Leave command selection and mutations to
the executor.
