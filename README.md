# Agent skills

Reusable workflows for coding and research agents. Requires Bun 1.3.14+ and Git. Node.js is not required.

| Skill | Purpose |
| --- | --- |
| `jj-clean-restack` | Rebuild a clean Jujutsu stack while preserving original history. |
| `jj-commit` | Write or refresh Conventional Commit descriptions and commit verified jj changes. |
| `jj-patch-stack` | Add fixes without rewriting existing changes. |
| `jj-repair-state` | Diagnose and repair damaged Jujutsu metadata. |
| `jj-review-restack` | Review, fix, and rebuild a Jujutsu stack. |
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

`jj-review-restack` requires `jj-clean-restack`. The checkout installer resolves
this dependency automatically. When invoking the upstream `skills` CLI directly,
select both skills explicitly.

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
