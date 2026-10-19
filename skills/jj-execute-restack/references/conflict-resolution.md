# Structural Conflict Resolution

Resolve the oldest affected rebuilt commit first. Use the redistribution map
and original milestones to distinguish mechanical overlap, incompatible behavior,
and missing dependencies. Revise the build order for dependency failures;
request clarification when intended behavior is ambiguous.

Use the plan's advisory preflight evidence when available. Resolve actual rebuilt
conflicts using the correction-child workflow below; predictions do not establish
behavior or ownership.

## Tool and inputs

Use Mergiraf for Rust content conflicts. jj merges and absorbs text, but its
external resolver receives complete base/left/right files. Mergiraf matches syntax
nodes within them, including some moves and extractions. That generates a
candidate; it does not establish behavior or commit ownership.

Check `jj --version`, `jj resolve --help`, `mergiraf --version`, and
`mergiraf merge --help` before use on an unfamiliar installation. The bundled
profile requires `--config-file`, `resolve -r`, its configured merge arguments,
and partial-conflict output support. CI pins Mergiraf `0.20.0` and jj `0.46.0`;
check capabilities on other versions.

If unavailable, resolve manually or install from the
[official options](https://mergiraf.org/installation.html) when authorized.
Loading this skill does not authorize installation or global configuration.

The scoped [profile](../assets/mergiraf.toml) enables full structural merging
instead of the built-in `--fast` mode, preserves partial output, and supplies
the path and marker length. Keep parse-error tolerance disabled. Use `merge`
through jj, not `mergiraf solve` on working-copy markers.

References: [Mergiraf usage with jj](https://mergiraf.org/usage.html#interactive-use-with-jujutsu),
[supported conflicts and limits](https://mergiraf.org/conflicts.html), and
[jj external merge tools](https://docs.jj-vcs.dev/latest/config/#3-way-merge-tools-for-conflict-resolution).

## Correction child, then fold

Apply the [mutation gate](scope-and-safety.md#mutation-gate), preserve unrelated
working-copy changes, and record the operation, destination, affected descendants,
and selected paths. Create and record a correction child; edit only that child.

```sh
jj --no-pager new "$DESTINATION" -m "Resolve the mapped structural overlap"
# Record CORRECTION explicitly after new; do not infer DESTINATION from @.
jj --no-pager resolve --list -r "$CORRECTION"
jj --no-pager --config-file "$SKILL_DIR/assets/mergiraf.toml" \
  resolve -r "$CORRECTION" --tool mergiraf 'root:src/example.rs'
jj --no-pager log -r "conflicts() & ($CORRECTION)" --no-graph \
  -T 'commit_id ++ "\n"'
jj --no-pager diff --from "$DESTINATION" --to "$CORRECTION" --git
```

`SKILL_DIR` is the absolute installed skill directory. Pass each literal path as
a separate quoted argument; `root:` selects from the repository root.
Explicit `--tool mergiraf` avoids launching an editor or TUI. A successful
invocation may leave conflicts: the conflict query must be empty before folding.
Use `resolve --list` only to inspect known conflicts; it errors when none remain.

Read the full candidate files, including comments, attributes, and regions outside
the old hunks. Compare with original milestones and remove unintended drift in
the child. Review both the correction delta and the candidate against the
destination's actual clean parent. Apply the
[per-commit validation protocol](validation-and-recovery.md#per-commit-check-protocol)
to the corrected tree, including affected callers, module wiring, and configurations.

Only when the child is conflict-free, verified, and wholly belongs to this
one destination:

```sh
jj --no-pager squash --from "$CORRECTION" --into "$DESTINATION" \
  --use-destination-message
```

Look up the rewritten destination by its recorded identity and revalidate it and
affected descendants oldest first. Further conflicts get their own correction
children. Verify original IDs and refs before advancing the clean bookmark;
emptied corrections are temporary material, not milestones.

## Failure and ownership boundaries

- On errors, timeouts, or parser fallback, inspect partial output and every
  selected file; earlier files may already be resolved. Keep the child and
  recorded operation. Do not fold, advance the bookmark, or retry unchanged
  inputs; continue manually or revise the plan using the available evidence.
- Binary files, file-kind/executable conflicts, and conflicts with more than
  two sides require native or manual resolution. Review deletion-versus-modification
  intent explicitly. Preserve alternatives; never select a whole side merely
  to clear a conflict.
- Cross-file moves, renames, signature/API changes, macro-sensitive changes,
  generated files, and ambiguous entity matches need project-level evidence.
  Carry edits to their intended locations with imports, callers, tests,
  visibility, and compatibility stages. Do not guess entity identities to
  obtain a clean merge.
- `jj absorb` follows line provenance, not semantic ownership. Use the explicit
  destination map and inspect resulting destinations and leftover hunks. When
  provenance disagrees, reconstruct corrections in each owner's earlier structure
  or split explicitly, then resolve descendants with this workflow. See
  [distributed fixups](reconstruction.md#distributed-fixup).

## Examples

### Extraction before a behavior change

Original base:

```rust
fn accepts(n: u32) -> bool {
    n > 10 && n % 2 == 0
}
```

The source stack changes the threshold to `20`, then extracts the condition
into `eligible`. The clean order extracts first, preserving threshold `10`,
then changes the helper to threshold `20`. Verify `accepts(12)` is true after
extraction and false after the behavior commit; `accepts(22)` remains true.
If Mergiraf cannot match the extraction, reconstruct this result manually.

### Correction across an extraction

A feature sets a threshold, a later refactor moves its condition into a helper,
and a fixup corrects the threshold. The mapped owner is the feature, even when
line provenance attributes the helper to the refactor. Reconstruct the corrected
threshold in the feature's earlier structure, then carry it through the
refactor. Both boundaries must pass their own tests; do not accept a partial
absorb that moves the assertion but leaves the corrected implementation behind.

### Move across modules

One source change moves `valid` from `parser.rs` to `decoder.rs`; another changes
`n >= 0` to `n > 0`. Inspect both paths and their original milestones, carry the
condition to `decoder.rs`, and include module declarations and callers. Keep
`parser`'s re-export if a recorded compatibility stage requires it. Verify zero
is rejected only at the behavior boundary and positive values remain accepted.
Per-file syntax matching does not establish this cross-file identity.

### Incompatible behavior

If the base returns retry count `3` and the two sides return `5` and `8`, leave
the conflict unresolved until original intent establishes the policy. Both
alternatives can compile. Neither concatenation nor choosing the larger value
is a justified resolution.

## Extension boundary

Other language profiles or backends can reuse the full-file input/output interface
and correction/validation contract. A tree-wide tool must additionally establish
cross-file identity and a path/entity-to-destination map, preserving deletions
and compatibility stages. Keep candidate generation separate from ownership and
history mutation; retain source preservation and final-tree equivalence.
No additional merger or backend framework is needed to reserve these extensions.
