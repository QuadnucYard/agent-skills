---
name: jj-commit
description: Write Jujutsu (jj) descriptions for merge-ready changes, development checkpoints, and experiments. Use for starting or finishing jj tasks, drafting messages, and rewriting stale or concatenated descriptions.
license: MIT
---

# JJ Commit

Write a concise Conventional Commit subject and a meaningful body grounded in
the actual change. Keep describing an existing change separate from finishing
the working-copy change. A request for a message alone authorizes drafting;
a request to redescribe a change authorizes applying its replacement description,
without committing or advancing the working copy.

## Red line: serialize description updates

Never update descriptions concurrently in the same repository, even for
different changes or from separate workspaces. Description rewrites can also
rewrite descendants; overlapping updates can create divergent changes. Use
one writer and await each description-changing command, including `jj describe`
and `jj commit`, before starting the next. Parallel inspection and drafting
are fine, but agents must hand drafts to the single writer. Before each write,
refresh the target's current commit ID and full description; if either changed
since inspection, reconcile the draft before applying it.

## Red line: stop on unexpected divergence

After each repository mutation, check for newly divergent changes. If unexpected
divergence appears after an operation, stop further mutations immediately.
Report the operation and affected changes, inspect the operation log and
divergent versions without changing them, and ask for the user's approval to
undo the offending operation. Do not automatically abandon a version, resolve
the divergence, or continue the task.

Only after explicit approval, undo the identified operation, taking care not to
revert unrelated or concurrent work. Verify that the prior state is restored
and the unexpected divergence is gone before proceeding with the task. If a
safe undo is unclear or divergence remains, stop and report the blocker.

## Choose the description by purpose

Use the intended destination of the individual change. Follow the user's
stated intent or the established workflow. Use the merge-ready form for
ordinary completed work intended to land. A stack can contain changes with
different purposes, and `jj commit` alone does not make a change merge-ready.

- **Ready to merge.** Explain the delivered behavior, why it matters, and
  consequential design decisions or constraints. Keep relevant evidence, such
  as a measured effect that justifies the design. Omit working plans, progress
  diaries, resolved blockers, amendment or fold instructions, and routine
  verification output. Report current verification separately.
- **Quick development to amend later.** Make the provisional status clear.
  Quick development usually follows a step-by-step plan. Reference the plan
  when it is available and identify the step or milestone this change covers.
  Capture progress, verified behavior, findings, deviations from the plan,
  open blockers, and the next step. If the plan is unavailable to the reader,
  give enough context to resume. Record the intended disposition when known.
  Use a stable jj change ID for a known dependency or fold target.
- **Exploration.** Start from the goal or question. Exploration usually leaves
  the method open. Record the approach actually tried and measured results such
  as runtime or compilation time. For a comparison, identify the exact baseline
  and candidate revisions or artifacts, and give the values, units, and change
  observed under comparable conditions. Include the command or setup needed to
  interpret the figures. Record negative or inconclusive findings and unavailable
  measurements honestly. Say what the evidence supports and where to find
  retained detailed output when it exists.

When preparing a provisional or exploratory change to land, rewrite its
description around the delivered result. Carry forward findings and measurements
that still explain or support the result. Preserve other useful context in the
source history or an existing report when available.

## Message conventions

- Use `type(scope): subject`; omit the scope when it adds no useful context.
  Choose the type by intent, such as `feat`, `fix`, `refactor`, or `docs`.
  Use an imperative subject, no trailing period, and aim for at most 72 columns.
- Always include a body, separated from the subject by a blank line. Explain
  the motivation and follow the guidance for the change's purpose. Avoid
  repeating the subject in longer words.
- Describe important design decisions, constraints, or tradeoffs when they
  explain the approach. Omit implementation inventories, helper names, file
  lists, and step-by-step mechanics unless they express an important technique
  or design decision the reader needs to understand.
- Use literal inline backticks for identifiers, commands, flags, paths, and
  code values when mentioned. Do not wrap ordinary prose in backticks. If a
  code span contains a backtick, use a longer backtick delimiter.
- Hard-wrap body prose at 72 columns, including bullet indentation. Break at
  word boundaries; keep code spans and URLs intact even if they exceed the
  limit. Preserve blank lines between paragraphs and before footers.
- Mark incompatible changes with `!` and a `BREAKING CHANGE:` footer that
  explains the impact and required migration. Add issue references only when
  known and relevant.

Example:

```text
fix(cache): isolate entries by workspace

Shared cache entries could leak settings between workspaces. Scope cache
identity to the workspace so each project retains its own configuration.

Keep `--no-cache` as an explicit bypass for troubleshooting.
```

## Describe or redescribe

For a describe or redescribe request, read
[references/redescribe.md](references/redescribe.md). Compare the existing
description against the target's current contents, consolidate squashed messages,
remove stale claims, and fully rewrite poor descriptions. Apply only the
description; do not finish or advance the working-copy change.

## Task and commit workflow

1. Before a new file-changing task, check `jj --no-pager status` and
   `jj --no-pager diff --git`. Require an empty diff, no conflicts, and no
   unexpected untracked files; a described empty change is clean. Finish
   authorized pending work after verification, or use a separate jj workspace
   from the intended base. Never discard or commit unrelated work to clean up.
   Requests to commit existing edits, draft messages, or only describe changes
   do not require an initially empty working copy.
2. Determine the change's purpose. Prefer `jj describe -m "planned message"`
   before editing to name the scope and motivation. For quick development,
   identify the plan step when one exists. For exploration, state the goal.
   Inspect existing edits first when continuing a task.
3. Review the target's full `jj --no-pager diff -r <target> --git`, status,
   and nearby `jj --no-pager log`. Reconcile the description with the actual
   result and intended destination; use the redescribe reference when replacing
   existing text.
   Commit only agreed work with jj, never `git add` or `git commit`. Do not
   reorganize history merely to write a message.
4. Run required tests and applicable checks against the exact content to commit;
   rerun affected checks after edits. Failed or skipped required tests and
   unavailable tooling block a merge-ready commit. An in-scope local
   checkpoint or experiment may record incomplete verification if repository
   rules allow the commit. Record what was checked, what is pending or blocked,
   and why. If no tests apply, say so and run applicable verification. Message
   drafting may proceed without claiming verification.
5. Commit the in-scope change at `@` with `jj commit -m "complete message"`.
   This creates an empty working-copy change. Prefer this over `jj describe`
   followed by `jj new`, even when a provisional description exists. For
   description-only requests, use `jj describe -r <target> -m "message"`
   without advancing `@`.
6. Read back the saved description, checking the revision, backticks, and
   newlines. Recheck status and diff: require a clean working copy before the
   next task, accounting for leftover edits and generated files without
   discarding unrelated work. A partial commit alone does not ensure cleanliness;
   no content changes need no empty completion commit. Report the change ID and
   verification separately. Description-only work preserves file trees and
   working-copy position as specified in the redescribe reference.

Always pass `-m` with the complete subject and body as one literal argument.
Preserve backticks and actual newlines through a process API or safe shell
quoting; never evaluate message text or launch an interactive editor.

PowerShell treats backticks as escapes in double-quoted strings; POSIX shells
can treat them as command substitution. Use shell-appropriate literal quoting:
PowerShell single-quoted strings or single-quoted here-strings, and POSIX
single-quoted strings. Handle embedded apostrophes according to that shell's
rules; double quotes and JSON serialization alone do not protect the message.
Never strip Markdown backticks to work around shell interpretation.

When literal quoting is uncertain, write the complete message to a temporary
UTF-8 file through a literal file-write API, then read it into a process argument
without a shell. For example, run this as a saved Python script:

```python
from pathlib import Path
import subprocess
import sys

message = Path(sys.argv[1]).read_text(encoding="utf-8")
subprocess.run(["jj", "--no-pager", "commit", "-m", message], check=True)
```

Pass only the temporary file's path to the script. For description-only work,
use `["jj", "--no-pager", "describe", "-r", target, "-m", message]` instead.
Keep `shell=False` (the default), await completion, and read back the saved
description to confirm literal backticks and paragraph breaks survived.

For signing failures, use only a repository-documented solution within existing
authorization. Otherwise stop, report the issue, and provide the full proposed
message in a code block. Do not repair or disable signing or invent a workaround.
