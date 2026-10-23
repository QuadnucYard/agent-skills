# Audit Results and Investigate Anomalies

Establish enough settings and execution context to interpret the result using
the settings/execution procedure. State which claims remain unverified when raw
data, logs, controls, or protocol history are unavailable. A summary table can
support a limited consistency review; it does not establish execution validity.

## Trace observations into reported conclusions

Reconcile the attempt inventory with the analyzed observations, including failures,
timeouts, retries, exclusions, and missing conditions. Trace each main reported
number from raw records through selection, transformations, joins, unit conversion,
aggregation, uncertainty estimation, and display. Check provenance/version links
before comparing values that may come from different runs or procedures.

Where feasible, independently recompute the consequential result or a justified
representative path. Use known-answer checks, direct raw-record inspection, or
an independent derivation to expose errors that rerunning the same script misses.
State the limits of sampled checks; do not claim every derived value was checked.

Inspect according to the actual analysis:

- Denominators, exposure, paired alignment, duplicated observations, weights,
  pooling, per-condition summaries, and transformations. Retain component values
  needed to interpret ratios and composites.
- Missingness, censoring, non-completion, outliers, exclusions, and replacement
  criteria, including whether they were selected after seeing outcomes.
- Independence, assignment, repeated measures, clusters, time dependence, and
  the source of uncertainty. Many correlated observations do not substitute
  for independent replication. Distinguish standard deviation, standard error,
  interval estimates, and variability across different experimental levels.
- Assumptions and uncertainty methods, effect sizes, practical thresholds,
  multiplicity, exploratory subgroup selection, adaptive sampling, and stopping.
  Quantitative results may be descriptive when inferential assumptions are
  indefensible; do not fabricate a suitable model from missing information.
- Sensitivity to plausible choices and important heterogeneity. An aggregate
  can conceal failures or reversals across tasks/units. Sensitivity checks need
  a stated question and bounds, not a search for a favorable answer.
- Figures/tables that mislead through units, direction, scale, omitted conditions,
  denominators, failure outcomes, or unexplained uncertainty. Ignore cosmetic
  preferences that do not change interpretation.

Map each central conclusion to the audited evidence. Separate observation,
inference, and explanation. Statistical detectability is not practical usefulness;
a nonsignificant difference is not equivalence. Equivalence/noninferiority claims
need justified margins and suitable analyses. Zero observed failures does not
establish zero failure risk. Restrict generalization to supported populations,
workloads, conditions, and periods; do not infer mechanisms from performance alone.

## Define and investigate the anomaly

Make the expectation explicit: invariant, control behavior, historical distribution,
forecast interval, practical threshold, or domain model. Record how the observation
was selected and whether the expectation was specified before seeing it. An
unexpected value is not automatically a faulty observation.

Triage the available evidence in this default order, adapting when a known
dependency makes another check more informative:

1. **Bookkeeping/analysis:** identities, units, joins, denominators, aggregations,
   stale outputs, omitted failures, or transcribed values.
2. **Execution/measurement:** wrong intervention/input, skipped work, invalid
   control, mismeasurement, contamination, interference, drift, or saturation.
3. **Design/comparison:** confounding, unequal selection/opportunity, carryover,
   interactions, an insensitive metric, or mismatch between sample and claim.
4. **Variation/selection:** dependence, sampling variability, multiplicity,
   optional stopping, and post-hoc selection of unusual observations.
5. **Domain explanations:** mechanisms consistent with the remaining evidence
   and the discriminating follow-ups needed to assess them.

This order is not proof of a cause, and multiple causes may coexist. Maintain a
compact explanation table with supporting/opposing evidence, a discriminating
diagnostic, predicted outcomes under competing explanations, cost/bounds, and
stopping criterion. Prefer the smallest informative check. Known-input/reference
tests and independent measurement paths are useful when a shared procedural bug
is plausible. Repeating the same condition answers a repeatability question;
it may not distinguish a phenomenon from a systematic error.

Track causes as supported, weakened, rejected within specified conditions, or
unresolved. Do not label a plausible environment issue as the established cause
without evidence. Preserve an anomaly that survives the recorded checks and
state residual uncertainty. Do not remove real rare failures by rerunning until
they disappear. Recommend prospective confirmation when a domain hypothesis was
generated by inspecting the surprising result.

Deliver scoped execution, comparability, and inference decisions separately.
Prioritize findings that change the central conclusion, then bounded repairs
or follow-ups that can resolve them. A justified "not assessable" with precise
missing evidence is preferable to an unsupported assurance or an invented cause.
