---
license: MIT
name: requirement-alignment-check
description: >
  Judge whether refined requirements faithfully preserve the user's original
  intent and adequately address ambiguities and acknowledged issues. Use when
  comparing a rewritten request, clarified specification, or acceptance criteria
  with the original request and subsequent user decisions. Review requirement
  alignment rather than implementation quality or delivery planning.
---

# Requirement Alignment Check

Evaluate two separate questions: **Does the refinement preserve the user's
intended outcome and constraints?** **Does it resolve, or explicitly account for,
the ambiguities and acknowledged issues that matter to that outcome?** A fluent,
detailed specification can fail either check.

Review meaning and observable behavior. Do not spend the review on formatting,
linting, or preferred wording. Review by default; edit the requirement only when
authorized. Suggested repairs do not constitute user agreement.

## Establish the authoritative source

- Read the original request, the proposed refinement, and available clarifications,
  corrections, examples, exclusions, and acknowledged issues. Identify the exact
  candidate being reviewed and cite source messages or document locations.
- Reconstruct the user's goal, intended users, required outcomes, constraints,
  priorities, exclusions, and completion criteria independently of the refinement.
  Preserve modality and scope: must, may, all, some, only, and unless can change
  the contract. Distinguish an illustrative example from an exhaustive rule and
  an explicit mechanism requirement from a suggested means to an outcome.
- Apply explicit later user decisions to the affected clauses, retaining earlier
  requirements that were not superseded. Treat competing stakeholder statements
  as conflicting unless the available decision authority resolves them. An agent's
  proposal, the candidate's assertions, and user silence are not confirmation.
- Separate confirmed obligations, necessary consequences, unresolved interpretations,
  proposed additions, and optional extensions. Existing behavior or domain evidence
  can reveal a constraint or conflict; it does not by itself authorize changing
  what the user requested. Inspect external context only where it can settle a
  material fact in the comparison.
- If the original, refinement, or consequential conversation is unavailable, request
  the missing input and continue checks supported by what is available. Identify
  the missing evidence; do not certify alignment from the refinement alone or
  reconstruct the original from it.

## Trace intent in both directions

Split compound statements into distinct obligations without losing their shared
conditions. For each source obligation, identify its counterpart in the refinement
and judge semantic coverage. For each substantive refined clause, identify its
source, explicit approval, necessary derivation, or status as a proposal.
Allow multiple clauses to express one requirement and one clause to cover several;
matching vocabulary or counting covered items does not establish alignment.

Check for:

- **Omission or substitution:** a requested outcome, exclusion, constraint, or
  affected user disappears, or a proxy activity replaces the actual outcome.
- **Weakened or narrowed obligations:** required behavior becomes optional,
  all relevant inputs become a convenient subset, or a guarantee loses conditions,
  failure handling, timing, or other qualifications that matter to the request.
- **Unsupported additions or restrictions:** the refinement invents mandatory
  features, technologies, thresholds, priorities, exclusions, or acceptance gates.
  Distinguish supported clarification and necessary consequences from discretionary
  choices. Keep helpful suggestions visibly optional until the user adopts them.
- **Changed meaning or inconsistent application:** actors, terms, units, data,
  triggers, states, exceptions, or dependencies change meaning across clauses.
  Check defaults, boundaries, lifecycle, permissions, failure behavior, and
  compatibility when the original outcome makes them relevant. Do not impose an
  unrelated domain checklist.
- **Scope hidden by deferral:** an agreed requirement is moved to unspecified
  later work or excluded under a release label. Preserve the complete agreed
  outcome. For foreseeable extensions, check decisions that would constrain them
  now and state what boundary remains open; do not turn speculative possibilities
  into mandatory features or prebuilt infrastructure.

Challenge apparent equivalence with concrete witnesses: could a result satisfy
the refinement while violating a source obligation? Could the refinement reject
an outcome the user explicitly allowed? The latter is a defect only when the
restriction lacks support; an approved clarification can legitimately narrow the
allowed outcomes. Judge observable semantics rather than sentence similarity.

## Audit ambiguity and acknowledged issues

Inventory ambiguities, contradictions, assumptions, and issues identified by the
user or explicitly recognized in the source discussion. Also flag newly discovered
material ambiguities, labeling them as reviewer findings rather than prior agreement.

For each item, establish the conflicting or plausible interpretations, affected
behavior, the refinement's treatment, and the evidence supporting closure. An issue
may be a defect, tradeoff, dependency, or limitation; acknowledging one does not
automatically require implementing a particular fix.

Use these dispositions:

- **Resolved:** the refinement selects a precise, consistent interpretation or
  specifies behavior that addresses the issue, supported by a user decision or a
  necessary derivation. Explain why it closes the issue and how to distinguish
  the intended result from the problematic one.
- **Explicitly open:** the refinement names the unanswered question or assumption,
  consequences, and dependent requirements. Credit that transparency without
  claiming resolution. A proposed interpretation remains provisional until there
  is adequate authority to adopt it.
- **Accepted or deferred:** the authorized decision records the limitation or
  deferral, its scope and consequences, and any condition for revisiting it.
  Preserve requirements that still belong to completion. Without that decision,
  a unilateral deferral remains open or misaligned.
- **Unaddressed or masked:** the item disappears, is merely repeated as a promise
  to handle it, or is silently converted into a settled choice. A note such as
  "consider edge cases" does not specify the affected behavior.

Test important ambiguous terms with at least two plausible interpretations that
would produce different outcomes. Require only the detail needed to distinguish
them. Do not invent numeric limits to make "fast" or "large" appear measurable.
Check that a claimed resolution propagates to definitions, dependent clauses,
exceptions, and acceptance criteria instead of creating a new contradiction.

## Check the acceptance criteria

Compare acceptance criteria directly with the authoritative source as well as the
refined clauses. For each material outcome or resolved issue, identify an input or
scenario and an observable result that would show whether it is satisfied. Include
the relevant boundary or failure case when it changes the user's intended result.

Criteria must distinguish success from the drift or ambiguity found in the review.
A checklist copied from the refinement can validate the wrong contract. Flag
criteria that omit required outcomes, reward only a proxy, or introduce unsupported
obligations. If criteria are absent, propose the minimum discriminating checks and
identify whether their expected results are grounded or still need a user decision.
This is a specification check; do not imply implementation tests have been run.

## Report the judgment

Lead with two explicit judgments:

- **Intent alignment:** aligned, misaligned, or indeterminate from available evidence.
- **Ambiguity and issue handling:** sufficient, sufficient only for named independent
  scope, insufficient, or indeterminate from available evidence. Distinguish a known
  unresolved issue from missing evidence about which issues exist. State when no
  material ambiguity or issue was identified within the available source coverage.

An affirmative overall judgment requires supported preservation of the complete
agreed outcome and sufficient handling of material issues. Explicitly open issues
may leave intent aligned while blocking adoption of the affected requirements.
Accepted limitations are sufficient only within the authority and scope recorded.
Do not hide a blocking omission or contradiction behind an aggregate score.

Provide a compact traceability table when several obligations or issues need to be
compared: source locator and obligation, refined locator, assessment, and gap or
closure evidence. Use a concise paired comparison for a small request instead.
Include supported matches as needed to establish coverage, not only defects.

For each substantive finding, give:

- **Evidence:** the source obligation or issue and the relevant refined clause
  (or its absence), with precise locations and brief quotations or paraphrases.
- **Consequence and scope:** a concrete behavior that would be wrong or undecidable,
  which requirements depend on it, and whether independent scope remains usable.
- **Repair:** the smallest faithful wording change, missing criterion, or focused
  user decision needed. Label proposed choices and preserve confirmed decisions.
- **Closure check:** what comparison, answer, or observable criterion would establish
  that the repair preserves intent and addresses the issue.

Consolidate shared root causes, order findings by impact, and distinguish confirmed
drift, open questions, and optional improvements. Ask only questions whose answers
could change the verdict or repair; continue independent checks while they remain
open. When no substantive findings exist, say so and state the source coverage and
evidence limits. Do not claim user approval, implementation readiness, or verified
behavior beyond what this comparison establishes.
