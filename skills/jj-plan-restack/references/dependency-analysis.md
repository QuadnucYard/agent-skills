# Dependency and Conflict Analysis

Use these standalone Nu scripts to find later file/hunk touches and predict
application conflicts. They read committed trees at a fixed jj operation with
`--ignore-working-copy`, leaving working-copy edits, history, refs, and
configuration untouched. Conflict checks use generated temporary files only.

Requires Nu and jj; tested with Nu `0.114.1` and jj `0.46.0` structured templates.
History and ordered conflict analysis also require Python 3.11+ (standard library
only). Conflict prediction needs Git `merge-file --diff-algorithm myers`.
Override executables with `--jj`, `--python`, and `--git`; on Windows use
`--python python` if `python3` is unavailable. No package manager, checkout of
this skills repository, or automatic tool installation is involved.

## Later touches and dependencies

Commands below assume the skill's `scripts` directory. Use absolute script paths
and `--repository PATH` when running elsewhere.

```sh
nu --no-config-file analyze-history.nu touches \
  --base BASE --tip TIP --change CHANGE --json
nu --no-config-file analyze-history.nu touches \
  --base BASE --tip TIP --change CHANGE --path src/example.rs --json
nu --no-config-file analyze-history.nu touches \
  --base BASE --tip TIP --change CHANGE --hunk h2 --json
nu --no-config-file analyze-history.nu touches \
  --base BASE --tip TIP --change START --path src/example.rs --whole-file --json
nu --no-config-file analyze-history.nu dependencies --base BASE --tip TIP --json
```

Revision expressions must select one revision; `BASE..TIP` must be linear.
`CHANGE` must belong to that range. Paths are exact repository-relative paths
using `/`, including spaces and fileset punctuation. Reads of `@` use its last
recorded snapshot, so prefer explicit original revisions.

`touches` follows edit spans through every subsequent delta, excluding diff
context and recording reverts individually. `--path` restricts source hunks;
`--hunk` selects an ID from a previous report. Hunk IDs are local to the source
snapshot and must be rediscovered after history changes. Ranges use one-based
`start` and `count`; zero counts denote insertion/deletion boundaries.

`--whole-file` follows the entire file at `START`, even if `START` did not edit
it. This mode requires `--path`, excludes `--hunk`, and also permits `START` to
equal `BASE`. The file must exist at the starting revision.

| Event relation | Evidence |
| --- | --- |
| `overlap` | Edit intersects tracked text or a deletion boundary. |
| `adjacent` | Edit touches a tracked boundary without intersecting it. |
| `same-file` | File changed outside the tracked text or metadata. |
| `rename` | jj reports a rename; tracking continues at the new path. |
| `metadata` | Executable mode changed. |
| `path` | Later change uses a path created, renamed, or copied by the source. |
| `uncertain` | Unsupported content, copies, or path reuse prevent reliable tracking. |

`dependencies` scans all source changes. Text, path existence, and executable
mode have separate anchors, so appending to a new file retains its creation
dependency, while mode changes do not claim unrelated text. Same-file and
adjacent edits alone do not create dependency edges. All edges are candidates:
semantic dependencies outside these textual/path relationships require review.

## Predicted conflicts

```sh
nu --no-config-file check-restack.nu --change CHANGE --onto DESTINATION --json
nu --no-config-file check-restack.nu \
  --base BASE --tip TIP --order order.json --json
```

`order.json` is an array of revision strings, an exact permutation of
`BASE..TIP`. Split/hunk reconstruction plans require manual destination mapping.
Feature extraction is not a permutation: do not pass a shortened selection as
an ordered check or treat a full-stack prediction as proof of retained-feature
independence. Use single-change checks only for mechanical evidence, with manual
dependency closure and exclusion mapping.
Ordered checks simulate original parent-to-change deltas from `BASE` and list
reversed dependency candidates in `reordered_dependencies`. Single-change mode
checks application only, without a stack-wide dependency inventory.

Full-file merges use `git merge-file --diff3 --diff-algorithm myers`. Add/delete,
executable changes, and file/directory collisions are checked at commit
boundaries. Native destination/source conflicts block simulation. Rename/copy
mappings, non-regular files, binary content, and failed merge tools produce
`unknown`. After an unresolved step, no subsequent commit is simulated;
`unassessed` lists those revisions, including empty commits that were not reached.

A `clean` result predicts text applicability, not behavior, semantic ownership,
or identical results from jj or Mergiraf. Keep manual semantic review in the
plan and per-commit validation in its execution requirements.

## Reports and coverage

Default output is a Nu record; `--json` returns machine-readable JSON with
`schema_version`, `mode`, `complete`, `events`, `issues`, and `limitations`.
History reports add `scope`, `hunks`, and candidate `dependencies`. Conflict
reports add `engine`, `destination`, `status`, `reordered_dependencies`,
`existing_conflicts`, `source_conflicts`, and `unassessed`. Labels use short jj
change IDs and descriptions; full commit/operation identities remain internal.
Command errors exit nonzero; findings such as `conflict` or `unknown` return a
report successfully, so inspect its fields.

`complete` describes textual/mechanical coverage. Empty events with incomplete
coverage do not establish that a hunk was untouched. Repeated text, deleted
lineage, copies, and reused paths require review. Exact removed fragments found
in other insertions are flagged as possible moves/extractions without guessing
entity identity. Hunk analysis supports UTF-8 and preserves CRLF and missing
final newlines.

Defaults: 500 commits (`--max-commits`), 1 MiB per collected file
(`--max-file-bytes`), 20,000 lines per file, and 25,000,000 old/new line pairs per
diff. File size is checked after reading a blob, not as a streaming memory cap.
Unsupported or oversized content yields explicit incomplete coverage.

Structural/entity or language-aware evidence can extend the typed snapshot
interface. Keep that engine separate from repository access, and retain manual
ownership decisions and the read-only contract.
