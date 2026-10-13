# Maintenance

## Verification

```sh
bun install --frozen-lockfile
bun run test
```

Tests run the pinned skills CLI in isolated project directories, check installed
skills and their resources, and install `jj-review-restack` alone.
GitHub Actions runs the same checks on Windows and Linux. Packaging verification
does not exercise live metadata repairs or evaluate a model's research critique.

Structural conflict integration has a separate behavioral suite:

```sh
bun run test:conflicts
```

It requires `jj`, `mergiraf`, and `rustc` on `PATH`. `RESTACK_JJ` and
`RESTACK_MERGIRAF` can select explicit binaries without changing global settings.
Fixtures use isolated temporary repositories and jj configuration; they compile
and run Rust behavior tests, check partial and refused resolutions, and compare
preserved source trees and refs. CI runs released jj `0.46.0` and Mergiraf
`0.20.0` on Windows and Linux. The ordinary installation suite remains usable
without these merge tools. Neither suite proves semantic equivalence for
arbitrary refactors; manual milestone review remains part of the skill.

The standalone history-analysis helpers have their own behavioral suite:

```sh
python -B -m unittest discover -s tests -p test_restack_analysis.py -v
```

It requires Nu, jj, Git, and Python 3.11+. `RESTACK_NU` and `RESTACK_JJ` select
explicit executables. Tests run copied skill scripts in isolated repositories
and check preservation, lineage, dependencies, and conflict predictions. CI runs
them on Windows and Linux and checks the Python helper/tests with `mypy --strict`.

## Shared guidance

`jj-review-restack` loads the separately installed `jj-clean-restack` skill.
The checkout installer adds that dependency automatically; direct upstream CLI
installs must select both. Keep the merge profile and conflict guidance inside
the canonical restack skill so its installed resources remain self-contained.
After editing that skill, run the installation, conflict, and analysis suites
listed under Verification.

Verification rejects missing references and installation tests check every
bundled resource. New skills go in `skills/<name>/SKILL.md`;
keep required resources inside each skill. Agent-specific metadata can go in
`agents/`. Plugin packaging can be added without restructuring these folders.

## Installer and sync scripts

`bun run install:skills <options>` installs from this checkout using the pinned
CLI. Defaults: all skills, Codex, project scope. Add `--global` for user scope and
`--yes` to skip prompts. It forwards other CLI options; `--source <URL-or-path>`
selects a different source. Project scope uses the caller's current directory.

`bun run sync:skills` pulls with `git pull --ff-only` and verifies the result.
Add `--install` followed by installer options to reinstall after pulling. It refuses
dirty worktrees and divergent history and never automatically commits or pushes.
Run `bun install --frozen-lockfile` after changing the lockfile. Review upgrades before changing the pinned
CLI dependency.

CLI installations are snapshots, even when agent directories use links. They do
not link directly to the development checkout. Reinstall after local edits;
GitHub installations can use the CLI's check/update commands.

## Migration record

Imported the skills from `.agents/skills`. Differing CC Switch copies were
preserved outside the repository during construction. Existing installations were
not overwritten or removed. Before migrating, compare and back up ordinary skill
folders and link targets outside discovery directories. Avoid competing managers
that maintain different copies of the same skill.

Packaging changes:

- Replaced the repair inspector's hard-coded Codex path with its installed skill path.
- Bundled clean-restack references in the review skill and included essential local
  jj guardrails, so an external workflow skill is optional.
- Resolved the patch skill's contradictory squash instructions in favor of its
  explicit additive-only contract: committed patches remain immutable.

The repository uses the MIT license. Each skill includes the license notice so
individual installations retain it. Before public release, review content for
anything that should remain private.
Private installs require configured Git or GitHub credentials; SSH sources work too.

References: [skills CLI](https://github.com/vercel-labs/skills),
[CLI documentation](https://skills.sh/docs/cli),
[Codex skill authoring](https://learn.chatgpt.com/docs/build-skills).
