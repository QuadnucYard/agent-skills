---
name: jj-commit
description: Write Conventional Commit descriptions and commit verified changes with Jujutsu (jj). Use when asked to write a jj commit message, describe a change, or commit with jj.
license: MIT
---

# JJ Commit

Write a concise Conventional Commit subject and a meaningful body grounded in
the actual change. A request for a message alone does not authorize committing.

## Message

- Use `type(scope): subject`; omit the scope when it adds no useful context.
  Choose the type by intent, such as `feat`, `fix`, `refactor`, or `docs`.
  Use an imperative subject, no trailing period, and aim for at most 72 columns.
- Always include a body, separated from the subject by a blank line. Explain
  the problem or motivation and the resulting behavior or high-level idea.
  Keep it short; do not repeat the subject in longer words.
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
  known and relevant. Describe delivered behavior, not speculative plans.
- Passing tests are a prerequisite, not a selling point. Never include test
  counts in the body. Omit routine test-pass statements, logs, and checklists;
  report verification separately to the user.

Example:

```text
fix(cache): isolate entries by workspace

Shared cache entries could leak settings between workspaces. Scope cache
identity to the workspace so each project retains its own configuration.

Keep `--no-cache` as an explicit bypass for troubleshooting.
```

## Commit workflow

1. Inspect the intended revision, its diff, and nearby descriptions with
   `jj --no-pager status`, `jj --no-pager diff`, and `jj --no-pager log`.
   Preserve unrelated work and commit only the agreed change. Never run
   `git add` or `git commit`; use Jujutsu for committing. Do not reorganize
   history merely to write a message.
2. Before committing, run the repository-required tests and relevant checks
   against the exact content being committed. All required tests must pass.
   Failures, skipped required tests, or unavailable test tooling block the
   commit; explain the blocker. If no tests apply, state that separately and
   run the repository's applicable verification. Rerun affected checks if the
   content changes after validation. Drafting a message can proceed without
   claiming the change is verified.
3. Apply the description only when requested. Use `jj describe -m "message"`
   to describe the target change without advancing the working copy; use
   `jj commit -m "message"` to finish the current change and create a new
   working-copy change. Never
   run bare `jj commit` or bare `jj describe`: they launch an interactive
   editor and can stall execution. Replace `"message"` with the complete
   subject and body, including actual newlines. Pass it as a literal argument
   through a process API, or use shell quoting that preserves backticks and newlines
   without evaluating message text. Never invoke an editor or interpolate the
   message into executable shell code.
   If committing fails because of signing, check for a solution documented
   in the repository. Follow it only within the existing authorization. If
   none is provided, stop and tell the user about the signing issue. Present
   the complete proposed description in a code block so the user can apply it.
   Do not attempt to repair signing, disable it, or invent a workaround.
4. Read back the saved description and confirm the intended revision and
   working-copy state. Check that backticks and line breaks survived. Report
   the change ID and verification outcome separately from the commit body.
