# Review a Restack Result

Review a completed or partially rebuilt stack against its source and intended
contract. Resolve explicit `BASE`, `SOURCE_TIP`, `CLEAN_TIP`, the fixed read
operation, and any corrected-source or extraction target. Read without
snapshotting the working copy. Do not move refs, repair commits, or write code.

Establish whether the result is complete. For a partial rebuild, record the
last validated milestone and any later unvalidated work separately. Apply the
final-target equality checks below only to a completed result. Compare a partial
result to that milestone's intended content and acceptance criteria, using its
recorded comparison tree when available. Account for the remaining target delta
as pending work; do not report planned, unbuilt features as dropped regressions.
Missing milestone evidence limits the review rather than establishing a pass.

## Establish what must match

Read the requirements, plan, source snapshot, feature/redistribution maps, and
execution evidence when supplied. Verify exact revision identities rather than
trusting mutable change IDs or a bookmark name. If records are missing,
reconstruct evidence from both histories and state what remains unverified;
never infer authorization for omissions from the result itself.

- History only: require source-to-clean tree equality.
- Authorized fixes: require equality to the verified corrected source and
  account for the complete original-to-corrected delta.
- Feature extraction: require equality to the independently prepared retained
  target and audit the full-source-to-target delta against retained/excluded
  ownership and dependency decisions. Follow [extraction scope](feature-extraction.md).

Read both summary and full content diffs, including binary, mode, generated,
and submodule changes where applicable. An empty final diff establishes content
equality only; it says nothing about useful boundaries or intermediate validity.
An explained extraction delta is expected, but an unexplained hunk is a defect.

For example, with exact recorded identities and `EXPECTED_TIP` resolved to the
appropriate target above, collect evidence without a working-copy snapshot:

```sh
jj --no-pager --ignore-working-copy --at-op "$OP" diff --from "$EXPECTED_TIP" --to "$CLEAN_TIP" --git
jj --no-pager --ignore-working-copy --at-op "$OP" log -r "$BASE..$CLEAN_TIP" --no-graph -T description
jj --no-pager --ignore-working-copy --at-op "$OP" diff -r "$CLEAN_COMMIT" --git
```

Repeat the last read for every clean commit; collect source descriptions and
parent diffs similarly. With extraction/fixes, also read the full source-to-target
delta separately, even when clean-to-target is empty.

## Review behavior and history separately

1. Read full descriptions and complete parent diffs in both histories. Reconcile
   every meaningful source hunk and milestone with a clean owner or a justified,
   authorized omission. Check later fixes, renames, merge resolutions, and
   descriptions for lost rationale or stale behavioral claims.
2. Review each result against its actual parent, oldest first. Trace its claimed
   contract through implementation, wiring, real consumers, errors, lifecycle,
   compatibility, and tests. Check coherent vertical slices, available prerequisites,
   shared ownership, and absence of unrelated behavior. Reject a broken commit
   repaired only by a descendant; a passing tip cannot validate its ancestors.
3. Compare meaningful migration, introduction, and removal states to the source
   timeline. For extraction, retained capabilities must work without the excluded
   ones; excluded behavior must not leak through retained shared support.
   If the original stack had conflicts, check whether they resulted from
   intentional feature removal. Reject resolutions that add intentionally
   removed features back, even when the rebuilt stack is conflict-free and tests
   pass. If removal intent remains unclear, ask the user and mark the affected
   resolution unverified.
4. Bind validation to exact revisions and parents. Reuse recorded checks when
   those identities and relevant conditions still match. For description-only
   rewrites, prove unchanged content and parent trees, map old evidence to the
   new identities, and review the new descriptions and graph. Rerun checks that
   depend on revision metadata; do not rerun behavior tests solely because a
   hash changed. Run missing or
   suspect behavior/build checks in an isolated workspace when authorized and
   available; report unavailable evidence. Do not spend review on format or lint.
5. Verify original commit identities and existing refs, safety/target tags,
   retained-prefix identity, and a separate rebuilt suffix rooted at the declared
   base. Inspect conflicts and unexplained empty or temporary commits. A declared
   no-op may share the original tip. Extraction with no rebuilt suffix may end
   at `REBUILD_BASE` with an optional fresh result bookmark; it still requires
   target verification and complete exclusion accounting. A stripped feature
   cannot remain in a reused prefix without an explicit valid removal milestone.

### Check for restack artifacts

Inspect full parent diffs and trace additions across the rebuilt sequence:

- Reject fixture-only commits unless they add new fixtures to establish baseline
  behavior or contain a large test change with several new test modules. Harness
  or test-execution changes are not fixture-only. Otherwise, propose combining
  fixtures with the implementation they test.
- Flag blank-line-only changes, including a single added or removed blank
  line, as restack artifacts. Include necessary blank lines in the relevant
  implementation change and remove unrelated edits.
- Flag code added in one place and moved in a later commit, including within
  the same file. This leaves the restack unclean: add the code at its final
  location in the introducing commit. Keep an intermediate location only when
  a required migration or compatibility stage needs it.

Cite the affected hunks and commits. Matching final trees and passing behavior
checks do not make these commit boundaries clean.

## Deliver findings

Give each defect its evidence, behavioral or reviewability impact, affected
short change IDs with descriptions, proposed semantic owner, and required
revalidation. Distinguish source defects, reconstruction regressions, plan/scope
errors, and missing evidence. Do not silently repair any of them during review.

Report separate conclusions for target content, behavior/design adoption,
intermediate boundaries, and source/ref preservation, followed by blockers and
verification limits. A partial result is reviewed only through its last proven
milestone; do not claim the unbuilt suffix passed. If repair is requested, update
the affected plan before execution and invalidate affected evidence according
to content, parent-tree, metadata, and check-environment changes.
