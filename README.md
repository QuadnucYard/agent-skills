# Agent skills

Reusable workflows for coding and research agents. Requires Bun 1.3.14+ and Git. Node.js is not required.

| Skill | Purpose |
| --- | --- |
| `code-review` | Review requirements, behavior, design quality, and change boundaries. |
| `experiment-design-and-audit` | Design experiments and audit settings, execution, results, fair comparisons, and anomalous outcomes. |
| `feature-planning` | Confirm design details and prioritize incremental features with effective tests and evidence-based confidence. |
| `feature-plan-review` | Audit feature boundaries, dependencies, complexity, and verifiable delivery; reject structurally unclear plans with a rewrite request. |
| `fix-commit-review` | Audit bug-fix claims, completeness, cost, scope, ownership, and reuse; separate existing defects from commit corrections. |
| `jj-execute-restack` | Execute a restack plan, apply authorized fixes, and verify the rebuilt stack. |
| `jj-commit` | Write or refresh Conventional Commit descriptions and commit verified jj changes. |
| `jj-patch-stack` | Add fixes without rewriting existing changes, then guide squashing after approval. |
| `jj-repair-state` | Diagnose and repair damaged Jujutsu metadata. |
| `jj-plan-restack` | Review a Jujutsu stack and plan boundaries, fixes, and validation without mutations. |
| `jj-split` | Split mixed jj changes into semantic commits, with existing-feature fixes and refactors first. |
| `recognize-stack-features` | Infer vertical features, real consumers, and dependencies across original commit boundaries. |
| `requirement-alignment-check` | Check refined requirements against original intent, ambiguities, and acknowledged issues. |
| `seminar-supervisor` | Critique arguments and designs for substantive defects. |
| `weekly-research-mentor` | Rehearse and review research updates. |

## Install

Select skills interactively:

```sh
bunx --bun skills add https://github.com/QuadnucYard/agent-skills --agent codex --global
```

Add `--skill '*'` to install everything, or `--skill '<skill-name>'` to select one.
Omit `--global` for a project installation; replace `codex` with your agent.
Private repositories require configured GitHub access. Use `--copy` if links are unavailable.
For npm-based environments, the same skills also install with `npx skills add <repository-url>`.

`jj-plan-restack` and `jj-execute-restack` install independently. Select both for
the complete workflow. They replace `jj-review-restack` and `jj-clean-restack`;
remove those old installations after switching to avoid competing workflows.

## Update

```sh
bunx --bun skills check
bunx --bun skills update
```

## Work from a checkout

From the repository directory, install everything:

```sh
bun install --frozen-lockfile
bun run install:skills --global --yes
```

Edit skills in the checkout and rerun the install command to use local changes.
To pull committed changes and reinstall:

```sh
bun run sync:skills --install --global --yes
```

Sync requires a clean worktree and fast-forward history. Run
`bun install --frozen-lockfile` again if the dependency lockfile changes.
Back up existing installations before replacing them.

Check each skill for tool prerequisites. Restart your agent if a newly installed
skill does not appear. See [maintenance notes](MAINTENANCE.md) for verification details.

## License

[MIT](LICENSE). License notices are included with each installed skill.
