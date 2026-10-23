# Software Engineering Experiment Guidance

Apply the sections relevant to the study alongside the shared contracts. These
are domain-specific threats, not a requirement to benchmark every tool or conduct
a participant study for every system. General non-software experiments do not
need this reference.

## Systems, algorithms, and benchmarks

**Work equivalence and correctness.** Before attributing performance, establish
equivalent intended work and output semantics with an oracle, invariants,
differential checks, reference cases, or task-quality measures. Check early exit,
no-op/skipped work, compiler-eliminated work, stale artifacts, failed requests,
and unintended cache hits. An intentional quality/resource tradeoff needs an
explicit multi-outcome comparison rather than an unconditional speed claim.

**Artifact and environment identity.** Capture relevant source/binary revisions,
build mode/flags, dependencies/runtime, hardware, resource limits, concurrency,
isolation, and external-service versions. Trace actual execution, not only saved
configuration. Assess shared load, scheduling, frequency/thermal state, memory
pressure, and runtime/device behavior according to the claimed effect. Do not
change system-wide settings merely because a generic benchmark checklist lists
them; justify relevant controls and preserve operating conditions needed by the
target use case.

**Preparation and timing.** Define startup, warmup/JIT/GC, state/cache reset,
setup/teardown, measured region, instrumentation overhead, and completion rules.
Distinguish cold-start from steady state and wall, CPU, and device time. Check
clock resolution and synchronization for asynchronous work: timing submission
alone can miss the actual work. Separate intentional caching effects from
accidental differences in preparation.

**Workload, load, and resources.** Define input size/distribution and provenance,
selection/tuning history, scaling dimensions, concurrency, and resource budgets.
Check whether the load generator saturates before the system, whether load is
fixed or arrival-driven, and whether request sampling misses stalled periods
(coordinated omission). Define latency distributions/quantiles, throughput,
errors, timeouts, and completed versus offered requests. Avoid comparisons that
change quality, load, and resources together without naming the resulting claim.

**Replication and generalization.** Distinguish iterations in one process,
fresh processes, builds, machines, workloads, and time periods. Match repetition
and uncertainty to the variation the claim spans. Pair/block/interleave where
useful while considering carryover; a fixed seed is not a universal replication
strategy. Benchmark-specific tuning can contaminate evaluation and narrow claims.
A microbenchmark does not by itself establish whole-application impact.

**Reliability and scalability.** Preserve failures, retries, non-completion, and
exposure denominators. Distinguish intentional fault injection from accidental
infrastructure failure and verify the fault was actually delivered. Define load,
problem size, resources, duration, and the scaling question. Successful-run-only
performance can conceal a stability regression.

## Developer tools and workflow studies

Define tasks, participants/teams, target experience/population, instructions,
training, allowed assistance, and task success/quality. Completion time alone
cannot establish productivity if correctness, difficulty, or review burden changes.
Use an assessment rubric and blinded assessment where feasible; distinguish
the metric from the broader construct it is intended to represent.

Account for experience, task difficulty, allocation, learning, fatigue, order,
team/repository clustering, contamination, and assessor expectations. A crossover
needs treatment/task ordering and carryover considered. Shared repositories or
participants who exchange solutions can create interference; repeated tasks by
the same developer are not automatically independent evidence.

For adoption/before-after comparisons, examine concurrent process/staff/workload
changes, time trends, self-selection, attrition, and spillovers. Distinguish
observational association from an identified causal effect. Record consent,
privacy, and applicable review prerequisites when participant data requires them.

Repository-derived proxies also need validation: counts of commits, issues, or
review comments are not direct measures of productivity or quality. Check bot
activity, identity duplication, project/version selection, and changes in logging
or repository practices before interpreting a trend.

## Simulation and generated tests

Separate verification that the simulator/generator implements its specification
from validation that the model, workload, or injected faults represent the target
system. Audit assumptions, parameter calibration, coverage, boundary behavior,
and sensitivity. Random seeds do not establish realistic sampling. Simulated
results inherit the scope limits of the model and input generation. Compare to
known cases, analytic invariants, or real observations where they can expose a
relevant mismatch.

## Methodological context

- [ACM SIGSOFT Empirical Standards](https://www2.sigsoft.org/EmpiricalStandards/docs/standards)
  provides study-type-specific evidence expectations for SE research.
- [Rigorous Benchmarking in Reasonable Time](https://kar.kent.ac.uk/33611/)
  discusses repetition at different levels and precision in systems experiments.
- [Google Benchmark user guide](https://google.github.io/benchmark/user_guide.html)
  supplies concrete examples of timing, warmup, interleaving, and harness behavior;
  this skill does not require that library or its defaults.
