# Evidence, Decisions, and Reports

Use these semantics in every mode. Keep records lightweight: prose and tables
are sufficient when they retain traceability. Do not require a tracker, service,
particular file format, or every field for an inconsequential detail.

## Claim and comparison record

For each central claim, identify:

- The decision it informs and purpose: exploratory, confirmatory, estimation,
  screening, optimization, or replication. Distinguish descriptive, predictive,
  associational, causal, and mechanism claims.
- Target population/system, selection of units/tasks/workloads, operating range,
  relevant time period, and limits of generalization.
- Treatment, comparator, intended contrast, and other intentional differences.
- Assignment unit, observation unit, independent replication/inference unit,
  pairing, nesting, and potential dependence or interference.
- Outcome construct and its operational measurement: formula, units, direction,
  denominator, window, aggregation, weighting, and primary/secondary role.
- Hypothesis or estimation target, practically meaningful effect/margin where
  relevant, uncertainty and decision rules, assumptions, and falsifying evidence.
- Needed controls, supporting artifacts, unresolved decisions, and alternatives
  that the comparison must distinguish.

Give records identifiers when needed to link many claims or artifacts; do not
create administrative identifiers that add no traceability.

## Evidence and attempt records

For a relevant setting or procedure, capture intended value/range, effective
resolved value, observed value, units, source locator, time/version, discrepancy
rationale, and affected comparison. Mark unknown states rather than guessing.
Useful locators include file/revision and line, command and log entry, raw record
identifier, allocation record, device readout, or dated operator note. Distinguish
contemporaneous evidence from a later recollection or reconstruction.

Link study/protocol revision, condition, independent unit, attempt, raw observation,
and derived result. Account for planned, attempted, completed, failed, excluded,
and never-started work. Link retries and replacements to originals; do not present
them as unrelated additional evidence. Record exclusion/correction reasons and
when they were decided. Preserve original evidence and label derived artifacts;
use immutable versions or checksums where they materially strengthen provenance.

## Findings and scoped decisions

Every substantive finding includes the evidence/location, affected claim,
consequence, repair or discriminating diagnostic, and how to verify the repair.
Classify its basis as confirmed defect, suspected risk, or missing evidence.
Give severity and confidence independently when useful: a serious consequence
can still depend on uncertain evidence. Missing records do not prove misconduct.

Keep these dimensions separate, and attach decisions to a named claim or use:

| Dimension | Dispositions |
| --- | --- |
| Planning readiness | Ready for the specified next step; conditional with named restrictions; blocked by a named decision/evidence gap |
| Execution | Consistent with the recorded checks; confirmed invalid for a specified use; unverified because required evidence is absent |
| Comparability | Comparable for the named claim; qualified for a narrower interpretation; non-comparable for that claim; unverified |
| Inference | Supported within stated scope and uncertainty; inconclusive; contradicted by assessed evidence; not assessable |

Execution consistency is not a guarantee of defect-free execution. "Contradicted"
requires evidence against the claim, not just missing support or a nonsignificant
test. A defect can invalidate one comparison while leaving another useful. Do
not globally block a sound narrow conclusion over unrelated missing evidence.

## Deliverables

For a **plan**, provide the operational question and claim map, design/comparison
matrix, measurement and analysis rules, collection/execution procedure, artifacts
to retain, resource/stop/recovery conditions, unresolved decisions, and readiness
for the next step. Distinguish required current work from optional follow-ups.

For an **audit**, lead with what the evidence can support and the decisive limits.
State assessed scope and evidence, reconcile material settings and attempts,
rank findings by their impact on interpretation, give scoped decisions, and
prioritize repairs. Distinguish additional records, auditable reanalysis, and
new experiments; do not claim one can substitute for another without evidence.

For an **anomaly investigation**, add competing causes, evidence for/against each,
bounded diagnostics with expected distinguishing outcomes, and unresolved causes.
Distinguish proposed diagnostics from executed ones and report actual observations.

Use compact reports for simple studies. Ask only questions whose answers affect
the design, interpretation, or next action. If data cannot be recovered, say
which conclusions remain unavailable and which observations are still reportable.
