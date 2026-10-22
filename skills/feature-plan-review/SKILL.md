---
license: MIT
name: feature-plan-review
description: >
  Review feature plans for actionable vertical slices, overloaded steps,
  design complexity, complete scope, and effective validation. Use to audit
  an existing feature plan or assess implementation readiness, rather than
  create a plan or review implemented code.
---

# Feature Plan Review

Assess whether the plan delivers the **complete intended feature** through
**coherent, verifiable increments**. Focus on **behavior and design adoption**,
not formatting or linting. Scale review depth to the actual risk.

## Establish the basis

- Read the plan, requirements, constraints, exclusions, and prior decisions.
  Separate **confirmed requirements**, **assumptions**, and **optional extensions**.
- Inspect relevant existing code, callers, contracts, and tests when available.
  Verify reuse and compatibility claims; do not invent paths or evidence.
- Request consequential missing inputs while continuing independent checks.
  Keep affected conclusions **provisional**; silence is not confirmation.
- Review only unless changes are authorized. Local plans are deliberately
  untracked: read them as review input, without investigating tracking status
  or rereading solely to confirm an authorized write.

## Audit the plan

- **Complete scope:** Map every requirement and material risk to a step and
  acceptance check. Trace success, failure, and state transitions across the real
  path. Check applicable permissions, data lifecycle, concurrency, compatibility,
  migration, rollout, and recovery. Required work cannot disappear into "later."
- **Design adoption:** Check actual callers, ownership, and integration. Flag
  unused abstractions, duplicate sources of truth, old paths left active, and
  incomplete migrations. Resolve consequential ambiguity before dependent work.
- **Complexity:** Compare with the simplest design satisfying the requirements.
  Challenge unnecessary layers, services, dependencies, configuration, frameworks,
  duplicate state, and temporary bridges. Identify the concrete burden and offer
  a simpler alternative preserving behavior and justified extension seams.
  Do not simplify away required safeguards or judge complexity by file counts.
- **Vertical slices:** Check each delivery step individually: does it deliver a
  narrow behavior through the necessary layers, with **observable effects now**?
  Name the entry point and changed result exercisable when that step completes.
  Dependencies and rollout gates are valid; reliance on later repairs is not. Flag
  sequences of "all backend, all frontend, then integration" and discovery followed by one
  giant build. Keep wiring and meaningful tests with their behavior.
- **Verification and validation (V&V):** For every step, require a concrete way to
  exercise its effect, expected before/after behavior, and evidence to retain.
  **Verification** checks the step's contract; **validation** checks its contribution
  to the intended user outcome. Gated and backend-only changes can be observed
  through an appropriate API, command, test, or demo. If evidence depends on later
  steps, reslice the work or justify bounded enabling work with its own check.
- **Overloaded steps:** Look for independent outcomes, decisions, risks, or checks
  bundled together. Split concerns that can be delivered or reconsidered separately
  without breaking each other. Keep one coherent cross-layer behavior together;
  more bullets or artificial layer splits do not improve delivery boundaries.
  Separate substantial independent refactoring and unrelated fixes where useful.
- **Actionability:** Each step needs an outcome, concrete actions, affected
  components or contracts, prerequisites, and observable acceptance criteria.
  Reference details elsewhere rather than demanding a fixed template. Enabling
  work and investigations need a bounded question or contract, evidence to collect,
  and the next behavior they unlock; they are not delivered functionality.
- **Ordering and intermediate states:** Expose hidden prerequisites and cycles.
  Investigate high-impact uncertainty before expensive dependent work. Keep
  intermediate states compatible and safe; assign temporary bridge removal and
  necessary cleanup to explicit steps. Challenge vague "finish everything" steps.
- **Priority and confidence:** Justify urgent, required-later, and deferred work
  using user value, actual constraints, dependencies, and cost of being wrong.
  Confidence needs evidence and a next check; it is separate from priority.
  Distinguish planned checks from completed checks. Optional deferrals need reasons,
  consequences, and reconsideration triggers. Do not invent deadlines or agreement.
- **Effective tests:** Require a meaningful setup, expected observable result, and
  plausible defect each check detects. Could it pass with the behavior broken?
  Flag implementation-mirroring assertions, no-crash checks, and mocks that hide
  the contract under review. Cover relevant boundaries and failures at appropriate
  test levels; avoid redundant coverage. Concrete manual checks can suffice for
  low-impact changes. Reviewing a plan does not require running future tests.
- **Future extensions:** Name foreseeable variation, the boundary accommodating
  it, and a concrete expansion trigger. Resolve decisions that constrain it now
  without prebuilding speculative machinery. Consider the full outcome; avoid
  version labels that conceal unexplained scope cuts.

## Report findings

Lead with **implementation readiness** and the specific steps blocked. Unresolved
work need not block independent ready slices; a small coherent feature may need
only one implementation step.

For each substantive root cause, provide **location and evidence**, **consequence**,
**blocking scope**, **concrete repair**, and **acceptance evidence**. Distinguish
confirmed defects, open questions, and optional improvements; order by consequence.
Do not turn preferences or unsupported possibilities into findings.

For overloaded or misordered work, propose **replacement steps in dependency
order**, each with an outcome, actions, **observable effects**, and **V&V checks**.
Preserve agreed scope and necessary safeguards. Rewrite only what findings require.

State evidence limits and remaining required decisions. If no substantive findings
exist, say so; do not invent objections or claim the feature itself is verified.
