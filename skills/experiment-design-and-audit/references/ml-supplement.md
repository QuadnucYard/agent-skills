# Optional ML Experiment Checks

Read only when ML affects the treatment, data selection, or evaluation. Apply
the shared experimental contract first. An ML-assisted developer tool still
needs the same task-quality, assignment, environment, execution, and result
checks as another tool; model-specific checks do not replace them.

- Record relevant model/checkpoint/service, prompt/template, retrieval corpus,
  tool versions, inference/training settings, and effective runtime behavior.
  Mutable services require version/time evidence and limits on repeatability.
- Trace data and split provenance, deduplication and unit of splitting, preprocessing,
  annotation, and train/tuning/evaluation exposure. Check leakage across related
  units and contamination from benchmark-aware tuning or model training where
  assessable. Unknown training exposure is uncertainty, not proof of leakage.
- Make tuning/search/selection budgets, stopping, checkpoint selection, and
  validation versus final evaluation explicit. Account for manual iterations,
  prompts, failed runs, and repeated evaluation when they can affect the claim.
  Separate equal-budget and best-available-condition comparisons as appropriate.
- Distinguish variability across training/generation, splits, tasks/examples,
  annotators, developers, and environments. Seeds alone neither establish
  independence nor capture every uncertainty source; choose repetition and
  analysis based on the target claim.
- Validate evaluation and annotation: rubric, judge version, blinding where
  feasible, consistency, and a reference or independently checked subset when
  it can reveal error. A model judge can share biases or contamination with
  the treatment and is not automatically a correctness oracle.
- Preserve errors, refusals, timeouts, retries, cost, latency, and task quality
  when relevant. Selecting the best of several generations changes the procedure
  and resource budget; disclose it instead of reporting it as one ordinary attempt.

Do not require datasets, seeds, GPUs, or model metrics in an experiment where they
are irrelevant. For general SE threats, use the software engineering guidance
already routed from the entrypoint rather than duplicating it here.

Further context: [NeurIPS paper checklist](https://nips.cc/public/guides/PaperChecklist)
on experimental details, variability, and compute reporting. It does not establish
that a particular experiment meets the shared validity criteria.
