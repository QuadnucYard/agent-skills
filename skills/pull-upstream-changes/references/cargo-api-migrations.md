# Follow an upstream Cargo crate API

## Identify the change

1. Find the dependency's declarations, including workspace inheritance,
   renames, feature flags, and source overrides. Identify the resolved package
   versions or Git revisions and the affected workspace consumers. Use
   `cargo tree --workspace -i <package-spec>` for reverse dependencies and
   `cargo tree -e features` when feature activation matters. Qualify package specs
   when multiple versions are present. Check relevant target-specific and
   optional callers, including tests, examples, and public re-exports.
2. Read the upstream migration notes, changelog, or source diff between the old
   and target revisions. Identify replacement APIs and behavior differences.
   Check the target against the project's Rust version and supported feature
   combinations. If the target requires a separate toolchain or public API
   change outside the request, surface that decision before adopting it.

## Update and verify together

- Update the owning manifest requirement or Git pin when needed. Use a targeted
  resolution such as `cargo update -p <package-spec> --precise <version-or-rev>`
  when the source and manifest allow it. Inspect the resolved graph and lockfile
  diff, account for solver-required changes, and follow the repository's lockfile
  tracking policy. Group crates that the resolver or callers require to update
  together. Use intermediate upstream releases only when they isolate a real
  migration boundary and produce a working checkpoint.
- Migrate the affected callers using the new contract. Preserve downstream
  outputs, errors, and defaults unless the requested migration changes them. Run
  checks for the affected packages and supported feature and target combinations.
  Start with `cargo check -p <consumer>` using the affected feature flags.
  Once that passes, exercise the behavior with a focused test such as
  `cargo test --locked -p client --test upstream_smoke preserves_fork_timeout`.
  Run the same assertion before and after the update. If the renamed constructor
  defaults to thirty seconds where the fork previously used ten, make the
  timeout explicit at the migrated call site and rerun the test.
- Commit the dependency resolution, caller changes, and any required regression
  coverage in the same checkpoint. Record the old and new resolved sources,
  deliberate behavior changes, and the consumer and feature checks run. Prefer
  locked verification for projects that track `Cargo.lock` so the checks exercise
  the resolution being delivered.
