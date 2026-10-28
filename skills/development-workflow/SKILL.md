---
name: development-workflow
description: >
  Coordinate software development from requirements through planning,
  implementation, behavioral review, and verified commits by selecting and
  connecting skills from this repository. Use for end-to-end development or to continue
  an existing development task at its current stage; focused requests retain
  their requested scope.
license: MIT
---

# Development Workflow

Connect this repository's skills into one continuous development task. Own the
transitions and completion accounting; let specialized skills own their
procedures. Enter at the stage the user needs, reuse established decisions and
evidence, and stop at the requested deliverable.

## Select the route

Inspect the request, conversation, repository instructions, working-copy state,
and available skill catalog. Establish the intended outcome, authoritative
requirements, accepted decisions, requested operations, and remaining work.
Distinguish planning, review, implementation, description-only, history, and
publication requests before making changes.

Read [skill routing](references/skill-routing.md) for the relevant route. Resolve
only skills shipped under this repository's `skills/` directory. When using an
installed copy, use the routing reference as the collection inventory and find
available copies by name. Read the selected `SKILL.md` before applying it and
only the supporting resources needed for the current operation. Honor explicit
choices among this collection's skills.

- Select one owner for each operation. Add complementary lenses only when they
  answer a distinct question; reuse their findings instead of repeating reviews.
- Match actual repository and language evidence. Detect `.jj` before choosing
  change-management commands; plain Git repositories do not require jj.
- Do not invoke this workflow recursively when another skill routes back to it.
  Resume the owning operation with the evidence already collected.
- A catalog entry is not proof that another skill is installed. If an essential
  named skill is missing, report the missing capability and continue independent
  work. Use another skill from this collection only when it preserves the required
  contract; otherwise leave the affected operation blocked. Never claim to have
  applied an unread skill or install dependencies without authorization.
- A skill added to this repository can join at a relevant operation without
  changing the whole workflow. Update the routing reference to describe its
  contract; keep specialized mechanics in that skill rather than copying them
  here. Keep all routing within this collection.

## Carry context between stages

Maintain a compact task record in the conversation or an appropriate local
artifact. Carry forward only what downstream work needs:

- Original requirements and source locations, exclusions, acceptance criteria,
  confirmed decisions, assumptions, and unanswered questions.
- The current deliverable, authorization boundaries, affected components or
  revisions, dependencies, and the next concrete action.
- Requirement-to-increment coverage, findings and their owners, checks actually
  run against identified content, and remaining completion gaps.
- For history operations, the selected skill's exact source snapshot, protected
  refs, revision mapping, and validation checkpoint.

Keep proposed decisions separate from confirmations, and planned checks separate
from executed evidence. Do not replace original requirements with an agent's
restatement or a review verdict. When inputs change, invalidate only affected
decisions, plans, and verification; retain evidence that still applies.

Local plan files are deliberately untracked. Do not investigate their tracking
status or reread them merely to confirm a write. Read a plan when its content is
needed for implementation or substantive review.

## Connect requirements, planning, and implementation

1. **Establish understanding.** Use `requirement-alignment-check` for a new or
   materially changed request, or to compare a refined specification with the
   original. Honor its confirmation requirement and reuse existing explicit
   confirmations. Request understanding does not authorize extra operations.
2. **Plan where design is needed.** Use `feature-planning` for new capabilities
   or extensions requiring design and delivery decisions. Carry confirmed
   requirements into its design dialogue; preserve its pending-decision gates.
   A localized repair with an established contract can proceed through focused
   investigation and relevant existing coverage or a focused regression check
   without a full feature plan.
3. **Review an implementation plan.** Use `feature-plan-review` for a supplied
   plan or a substantive plan just produced for implementation. Feed structural
   findings back into planning; compare changed requirements with their original
   sources when needed. Continue independent work while decisions are pending.
4. **Execute authorized increments.** Inspect real callers, contracts, and
   repository conventions, implement a coherent slice, and exercise the real
   behavior. Keep wiring, migration, and necessary tests with their owning
   behavior. Report a blocker when required evidence or tooling is unavailable.

Cover the full intended outcome and interactions. Resolve correctness gaps now,
and name justified extension boundaries and their reconsideration triggers
without building speculative machinery. Name increments by outcomes rather than
release shortcuts such as `V1`. An accepted early increment does not waive the
remaining requirements.

For a bug fix, establish the violated contract and root cause before choosing a
repair. Use a discriminating regression check when warranted. For performance
claims or uncertain experimental results, take the experiment route before
treating a measurement as a design decision.

## Connect verification, review, and commits

Use `code-review` to check the resulting behavior, requirements, actual adoption,
and simplification. For a repair-focused audit, let `fix-commit-review` own the
repair's validity, completeness, cost, and ownership; supplement only general
conformance or adoption checks it has not already covered. Associate findings
with their owning increment and acceptance impact. Review-only requests deliver
findings; they do not authorize fixes or history changes.

During authorized implementation, repair in-scope defects and required omissions,
then recheck affected behavior. Return to requirements or planning when a finding
changes a contract or dependency. Required follow-ups remain completion gaps;
optional refinements do not silently expand scope. Re-review only affected paths
unless new evidence widens the risk.

Reviews focus on behavior and design adoption, not formatting or linting. Run
required repository checks as execution verification, keeping their results
distinct from design judgments. Use tests that can expose a plausible defect;
do not add tests merely to mirror an implementation or the wording of a document.

Finish each verified, coherent unit with the repository's commit workflow when
committing is requested or required by standing instructions. In jj repositories,
use `jj-commit` for ordinary task boundaries and descriptions. A specialized
history workflow owns its topology and commit destinations; do not apply a
generic finish command that would violate it. Serialize repository mutations,
including description updates across workspaces. Use literal message arguments
and preserve configured signing.

In a plain Git repository, follow its conventions and commit only task-owned
changes when authorized. Message-only requests authorize drafting, not staging,
committing, or pushing. Include a meaningful explanation of motivation,
resulting behavior, and consequential design decisions when required by the
user or repository.

Before delivery, account for the requested outcome, remaining blockers, executed
verification and its limits, and resulting commit IDs or history artifacts.
Do not create empty commits for read-only or no-op work. Publishing, messaging,
pushing, or replacing refs requires applicable authorization; permission to
develop or commit locally does not imply it.
