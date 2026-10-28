# Describe or redescribe a jj change

Use this workflow for an existing change, including descriptions concatenated
by squash, made stale by fixes, or left behind after content was split out.
Use the shared message rules in `SKILL.md` for new descriptions and replacements.

1. Run `jj --no-pager status` to snapshot current working-copy edits, then
   resolve the requested revision to one unambiguous change and record its
   change ID and current commit ID. Use `@` only when the working-copy change
   is the intended target. For multiple requested changes, inspect and describe
   each separately; do not apply one shared message to a whole revset.
2. Read the target's full description with
   `jj --no-pager log --no-graph -r <target> -T description` and its complete
   diff with `jj --no-pager diff -r <target> --git`. Inspect nearby history
   and the target's file contents as needed to understand behavior and intent.
   For a non-working-copy target, use that revision's contents, not unrelated
   files at `@`. For merges, `diff -r` compares against the merged parents;
   inspect the parents when the merge itself is the point of the change.
3. Compare every substantive claim in the old description with what the
   target currently delivers relative to its parents. Treat the old text as
   context, not proof. Identify surviving intent, newly added behavior,
   removed or split-out work, and superseded approaches. Read relevant code,
   documentation, and tests before asserting behavior; consult prior versions
   only when they help recover a rationale that still applies. Do not invent
   motivations or carry unsupported claims forward.
4. Write one coherent description of the resulting change. Consolidate
   squashed messages around the combined outcome, remove repetition and
   obsolete claims, and reflect fixes and the scope remaining after a split.
   Reconsider the type, scope, subject, body, breaking-change notice, and
   references rather than preserving the old subject by default. Preserve
   still-valid rationale and relevant provenance or required trailers. If the
   existing writing is poor, fully rewrite it; do not merely polish or append
   a correction. Keep a sound, accurate description unchanged when rewriting
   adds no value.
5. Handle gaps honestly. An empty change must not claim removed behavior;
   distinguish an intentional empty marker or merge from an implementation
   change. With unresolved conflicts, describe only established intent and
   current limitations, without claiming completion. Ask for missing intent
   only when it materially affects the description and cannot be recovered.
   Description-only work does not require rerunning code tests and must not
   imply new verification; the commit test gate in `SKILL.md` applies to committing content.
6. Apply updates serially through one writer, following `SKILL.md`'s red line;
   never run description updates concurrently, even for different targets.
   Before applying, confirm the target's commit ID and full description have
   not changed since inspection. If either changed, reread the description and
   recheck the content before reconciling the draft. Record the target
   and descendant file-tree identities before applying for comparison after. Use
   `jj describe -r <target> -m "message"` with the safe literal argument handling
   in `SKILL.md`'s commit workflow. Never use `jj commit`, edit files, split, squash, or restack just to
   repair a description. A metadata rewrite changes commit IDs and can rewrite
   descendants; do not bypass immutability or rewrite published history without
   authorization. If blocked, provide the replacement text and explain why it
   was not applied.
7. Read back the full saved description by change ID and inspect status.
   Confirm that target and descendant file trees remain unchanged and that
   the working copy did not advance. Report the target change ID, replacement
   description, and any unresolved limitations separately from the message.
