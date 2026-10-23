# Audit Settings, Comparisons, and Execution

## Reconstruct the existing study

Start with what the experiment actually specified and ran, preserving its original
question and scope. Separate a defect in that experiment from an enhancement
that would answer a different question. Inspect protocols, configurations,
procedures, scripts, allocation records, logs, instruments, and raw outputs as
available. Do not replace missing historical evidence with an idealized protocol.

For each material setting, reconcile intended, effective/resolved, and observed
values using the shared evidence record. Inspect defaults, inheritance,
configuration precedence, manual actions, and hidden preprocessing/selection.
Establish version and time relevance: today's file may differ from the procedure
used for an old result. Preserve conflicting sources and unknown states; a
document or later recollection is not automatically runtime evidence.

## Assess fairness against the claim

Build a comparison matrix covering the relevant treatment/comparator, inputs and
selection, materials/versions, preparation, resource/access allocation, environment,
operators/participants, order/time, measurement, termination, optimization/tuning,
and analysis. Classify material differences as:

- The intended treatment or contrast.
- Controlled, blocked, paired, randomized, or otherwise accounted for.
- Justified for the specific question and transparently reported.
- A confounder or an unresolved comparability question.

Fairness does not mean every setting must be identical. Equal-resource comparisons,
recommended-operating-condition comparisons, and component-attribution studies
answer different questions. Equivalent opportunities can require different
numeric parameters. Explain asymmetries, tuning/preparation/selection costs,
and what the comparison estimates. Report separate comparisons when materially
different fairness definitions matter; do not silently switch between them.

Check comparator relevance and competence. A malfunctioning baseline is an
execution defect; an obsolete or intentionally restricted baseline may instead
limit the question. A published reference number can provide context without
being a directly comparable measurement. Do not infer direct comparability
from similar metric names.

## Verify actual execution

Before interpreting the treatment effect or an abnormal observation:

1. **Reconcile attempts.** Compare planned conditions and units with attempted,
   completed, failed, excluded, duplicated, interrupted, replacement, and missing
   work. Check allocation, order, collection, and stopping deviations.
2. **Verify identity.** Link treatment/version/material, inputs/sample/unit,
   instrument/environment, allocation, attempt, and raw output. Check stale or
   cross-run artifacts and mismatched records.
3. **Verify delivery and work.** Establish that the intended intervention was
   delivered and the intended work occurred. Successful exit, a plausible number,
   or a completed form alone does not prove this.
4. **Verify measurement and integrity.** Assess controls, calibration, timing,
   logging, valid ranges, units/conversions, environmental drift, saturation,
   contamination, and condition-specific failures according to the actual risks.
5. **Scope consequences.** Mark affected executions and comparisons using the
   shared dispositions. State exactly which checks were possible and their
   evidence limits; do not imply complete exclusion of execution defects.

For negative, null, or unexpectedly good results, verify that the procedure
could detect the effect or failure it was intended to measure. A missing effect
can reflect an insensitive measure or failed manipulation, but that possibility
is a diagnostic hypothesis until checked.

## Preserve failures and distinguish recovery actions

A crash, timeout, refusal, non-completion, or instability under valid conditions
can be a genuine treatment outcome. Distinguish it from an infrastructure or
procedure failure using evidence. Exclusion and rerun criteria must be justified
against the target claim and applied symmetrically, not selected because an
observation is inconvenient. Missingness or failures related to treatment can
bias a successful-completers-only comparison.

Preserve originals and separate:

- **Reanalysis:** change/check the processing of existing raw observations.
- **Remeasurement:** measure the same experimental unit again; this does not
  necessarily add independent evidence or undo irreversible changes.
- **Rerun:** repeat an execution under specified conditions; preserve linkage and
  distinguish deterministic replay from new stochastic evidence.
- **New independent collection:** add new experimental units under a defined
  protocol; check selection, cost, and whether the original question changes.

A successful rerun does not retroactively validate an old attempt or eliminate a
rare real failure. Repeated runs of the same broken harness can reproduce a bug.
Bound recovery work by an explicit question, budget, stop condition, and existing
authorization. Where evidence is unavailable, report the uncertainty and the
minimum additional record or experiment that could change the disposition.

For every proposed repair, state whether the existing evidence supports a narrower
claim, an auditable reanalysis suffices, additional records might resolve the issue,
or a new experiment is required. Do not assume post-hoc adjustment repairs a
design confounder without a defensible identification argument.
