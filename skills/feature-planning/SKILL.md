---
license: MIT
name: feature-planning
description: >
  Design software features and turn requirements into actionable, incremental
  implementation plans with user-confirmed design details, feature priorities,
  evidence-based confidence, and effective tests.
  Use when planning a new feature, extending existing behavior, or breaking
  a feature proposal into verifiable delivery steps.
---

# Feature Design and Planning

Consider the complete intended feature, then build toward it through small,
verifiable increments. Do not attempt to deliver the entire product in one
implementation step. Scale planning detail to the feature's complexity and risk;
avoid turning a small change into an architecture project.

## Establish the outcome and boundaries

- Identify the user's problem, expected observable behavior, scope, constraints,
  and completion criteria. Separate requirements from assumptions and optional
  extensions. Surface unresolved decisions for the design dialogue below;
  continue independent investigation while they remain unresolved.
- Inspect the existing implementation, callers, interfaces, and relevant tests
  before proposing replacements or new abstractions. Identify what can be reused
  and where current behavior must remain compatible.
- Consider the full path from input to result, including relevant failure modes,
  data lifecycle, permissions, integration, migration, and rollout. Address risks
  that affect correctness now; explain why a concern can be deferred when its
  omission would otherwise leave a gap in the design.
- Make foreseeable extension points explicit: what is likely to vary, which
  boundary accommodates it, and what change would justify extending that boundary.
  Reserve these paths through clear ownership and contracts. Do not prebuild
  speculative frameworks, configuration systems, or unused generalizations.

## Keep proposed additions outside the mainline

Trace proposed behavior and constraints to the user's raw requirements, prior
confirmed decisions, or an established contract. If an addition goes beyond that
basis, ask the user whether it belongs in scope before treating it as required.
This includes agent-proposed resource budgets, quotas, performance targets, and
configurable limits; their usefulness alone does not establish a requirement.

Keep unconfirmed additions in a separate proposal list with their rationale,
tradeoffs, and pending decision. Do not assign them urgent or required priority,
mix them into the main delivery sequence or acceptance criteria, or make them
prerequisites for independent requested work. For nontrivial additions, discuss
the design alternatives and consequences before requesting a scope decision;
approval of the general goal does not settle the added constraint or its value.
If accepted, confirm design and priority before integrating the addition.

Distinguish optional additions from safeguards needed to satisfy existing
requirements or contracts. Show the dependency and evidence for a necessary
safeguard; if it introduces a new product policy or an unresolved limit, ask the
user to decide it and block only the work that depends on that decision. Keep
foreseeable extensions visible without making them current delivery obligations.

## Grill and confirm every design detail

Treat design as a dialogue with the user. For every design detail, ask the user
to explicitly confirm the decision before treating it as settled. Existing explicit
answers count as confirmation; do not repeatedly ask about unchanged decisions.

- Keep a decision record with the question, concrete proposal or alternatives,
  rationale, and status: confirmed, pending, or conflicting. Cover behavior and
  exclusions, interfaces, data semantics, permissions, failures, compatibility,
  migration, rollout, extension boundaries, priorities, and acceptance criteria
  wherever they apply. Include the decision to defer or omit a concern.
- Ask focused questions in manageable batches. Explain the tradeoff and offer a
  recommendation when evidence supports one. Use available question tools or
  direct conversational questions, and wait for the user's answers. A generic
  request to approve the whole plan does not confirm its individual details.
- Do not accept ambiguous terms such as "fast," "large," or "handles errors."
  Ask for concrete inputs, outputs, limits, units, examples, and failure behavior
  until the interpretation is unambiguous. Expose contradictions and obtain a
  decision; do not silently choose an interpretation or invent requirements.
- Silence, elapsed time, a preselected answer, and the agent's confidence do not
  count as confirmation. Mark unanswered questions as pending and block work that
  depends on them. Continue only independent investigation or already confirmed
  work. Present a provisional plan while questions remain; never call it agreed.
- Unknown empirical facts can have bounded investigations, but confirm their
  questions and decision rules. If findings require a new or changed design
  decision, return to the user. Preserve prior confirmations that still apply.

## Choose a proportionate design

Prefer the simplest design that satisfies the complete current requirements and
keeps justified extensions possible. Compare alternatives only where a material
tradeoff exists. Explain consequential choices using existing constraints and
evidence, including migration cost or reversibility where relevant.

If uncertainty could invalidate the architecture or ordering, schedule a bounded
investigation with a specific question, evidence to collect, and a decision it
will unlock. Distinguish its findings from delivered functionality; remove or
integrate exploratory code deliberately. Avoid open-ended research and abstractions
whose only justification is that they might be useful someday.

## Prioritize capabilities and uncertainty

Assign each capability a priority and explain it using user impact, actual timing
constraints, dependencies, and the cost of being wrong. Confirm these assignments
with the user rather than inventing deadlines or business urgency.
Apply delivery priorities only after establishing scope; uncertainty or potential
value does not promote an unconfirmed addition into urgent mainline work.

- **Urgent:** needed for the immediate user outcome, a prerequisite that blocks
  useful progress, or an investigation that could invalidate expensive later work.
  State why it must happen now and the smallest useful result it can deliver.
- **Required later:** part of the agreed complete feature, but safely sequenced
  after earlier increments. Give it a concrete delivery step and acceptance check.
  Lower urgency does not remove it from completion criteria.
- **Deferred:** optional work or a user-confirmed scope change whose current value
  or design is too uncertain to justify building now. Record the uncertainty,
  consequence of deferral, evidence needed, and a concrete reconsideration trigger
  such as a resolved dependency, measured threshold, or confirmed user need.

Priority and confidence are separate judgments. A low-confidence decision with a
large downstream impact may require urgent investigation. An uncertain optional
extension may be deferred. Do not defer essential correctness, permissions, data
integrity, or their acceptance checks merely because they are difficult or unclear.
Reduce uncertainty with a bounded check, or obtain an explicit scope decision.
Keep deferred work visible without implementing speculative support for it.

## Build an ordered sequence of increments

- Begin with the smallest coherent behavior that can be exercised through the
  relevant real path. Expand capability and integration step by step toward the
  full outcome. Name steps by the behavior or decision they deliver.
- Discovery followed by one step containing all functionality and a final cleanup
  step is still one-shot delivery. Split the implementation itself into working
  increments. Keep incomplete paths gated until their required safeguards work;
  incremental development does not require exposing unfinished behavior to users.
- Prefer working slices across the necessary layers. Avoid a sequence consisting
  only of all data structures, then all services, then all UI, with no observable
  result until the end. Necessary enabling work must state which next behavior it
  unlocks and how its contract can be checked independently.
- Order prerequisites explicitly. Bring forward cheap checks of high-impact
  assumptions; keep later steps from depending on unresolved guesses. Split any
  step that hides several independently risky changes or has vague completion
  criteria. Do not manufacture steps that add no meaningful outcome or evidence.
- Keep intermediate states coherent and compatible. Identify temporary bridges,
  migration ordering, gating, cleanup, and recovery when needed. Assign removal of
  temporary mechanisms to a concrete step so they do not become permanent debt.
- Map every current requirement and material risk to a delivery step and a check.
  Deferring an agreed requirement to an unspecified future effort does not complete
  the plan. Keep optional extensions separate from required completion work.

For example, a data export can first download a small authorized result behind a
gate, then expand to complete traversal and failure handling, then establish the
supported scale. Each increment exercises the real export path; grouping all
backend work before all frontend work does not provide that progression.

For **each step**, provide:

1. **Outcome, scope, and priority:** the observable behavior or resolved uncertainty,
   affected boundaries, prerequisites, and why it belongs at this point in the plan.
2. **Actions:** concrete changes, in enough detail that implementation can start;
   identify relevant components without inventing uninspected file paths.
3. **Acceptance and tests:** observable completion criteria, discriminating checks,
   and any relevant failure or compatibility case.
4. **Confidence:** low, medium, or high, with supporting evidence, remaining
   uncertainty, and the next check that could increase or reduce confidence.

Use confidence as a reasoned judgment, not a fabricated probability. High means
direct evidence supports the approach and important risks have effective checks;
medium means the approach is supported but a material assumption remains untested;
low means missing evidence could change the design or sequence. Distinguish planned
checks from checks already performed. A confident design is not a verified result.

## Plan tests that can expose defects

- Tie each check to a requirement, risk, or plausible regression. State the input
  or setup, expected observable result, and the defect it would detect. If a test
  would still pass with that defect present, strengthen its assertion or replace it.
- Check behavior through the appropriate public boundary. Choose unit tests for
  isolated rules, integration tests for real contracts, and end-to-end tests for
  critical user paths; use only the levels the risk justifies. Reuse good coverage
  instead of duplicating it at every layer.
- Include meaningful boundaries and failure paths where applicable, such as empty
  input, invalid state, permissions, partial failure, retry, or migration of existing
  data. Select cases from the design's actual risks rather than a generic checklist.
- Keep expectations independent of the implementation. Do not recompute the answer
  with the same algorithm under test, assert only that execution did not crash, or
  mock away the integration whose behavior needs verification. Use controlled
  dependencies when needed, while preserving the contract being tested.
- Match effort to impact. Avoid brittle assertions about internal call order,
  snapshots without a behavioral purpose, and tests that merely mirror code.
  Identify manual or exploratory checks when automation would add little value;
  say what evidence they should produce and what remains unverified.

## Deliver and evaluate the plan

Present the intended outcome, confirmed design decisions, ordered steps with
their priorities, tests, and confidence, and the explicit extension boundaries.
List deferred capabilities with reasons and reconsideration triggers. Keep pending
questions visible and dependent steps provisional. Do not impose a fixed number
of stages or leave the final step as an unexplained instruction to finish
everything else.

When writing a local plan file, treat it as deliberately untracked. Do not check
its tracking status or reread it solely to confirm the write.

For a planning-only request, deliver the plan without implementing the feature.
When implementation is authorized, execute one increment at a time, inspect the
result, run its checks, and update confidence before progressing. Passing checks
must support the claimed behavior; failures or contradictory evidence require
fixing the step or revising dependent steps. Report the remaining gap to the full
outcome. Reconfirm new or changed design details with the user before dependent
implementation; proceed with unchanged, already confirmed decisions.
