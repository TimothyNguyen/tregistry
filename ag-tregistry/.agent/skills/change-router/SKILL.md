---
name: change-router
version: 0.1.2
description: |
  Routes changed files to the appropriate agent roles using agents/routing.json.
  Given a git diff, file list, or PR changeset, outputs a dispatch plan mapping
  each changed area to the correct agent (swe, qa-agent, migration, data, cloud,
  design-agent, spec-agent, orchestrate). Invoke when coordinating multi-agent
  work on a PR or large feature branch.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [orchestrate]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Change Router

Maps changed files to the appropriate agent roles and produces a dispatch plan.

## Usage

```bash
# from git diff
node scripts/dispatch-on-change.mjs --git-diff HEAD~1

# from file list
git diff --name-only origin/main | node scripts/dispatch-on-change.mjs

# from explicit file
node scripts/dispatch-on-change.mjs --files /tmp/changed.txt

# write plan to file
node scripts/dispatch-on-change.mjs --git-diff HEAD~1 --output /tmp/plan.json

# also write subagent manifests to .architecture-agent/subagents/
node scripts/dispatch-on-change.mjs --git-diff HEAD~1 --manifests
```

## Routing Rules

Rules are defined in `agents/routing.json`. First matching rule wins per file.

| File Pattern | Agent |
|---|---|
| `tests/**`, `**/*.test.*`, `**/*.spec.*` | `/qa-agent` |
| `**/*.sql`, `migrations/**` | `/migration` |
| `**/*.tf`, `**/*.hcl`, `Dockerfile`, `.github/workflows/**` | `/cloud` |
| `**/*.py`, `**/*.ipynb`, `databricks.yml` | `/data` |
| `**/*.cs`, `**/*.sln`, `**/*.csproj` | `/swe` |
| `**/*.tsx`, `**/*.css`, `components/**` | `/design-agent` |
| `docs/**`, `**/*.md`, `rfcs/**` | `/spec-agent` |
| `agents/**`, `scripts/**`, `core/**` | `/orchestrate` |
| `**/*.ts`, `**/*.js` | `/swe` |
| _(anything unmatched)_ | `/swe` |

## Output Format

```json
{
  "totalFiles": 12,
  "agents": [
    {
      "name": "swe",
      "invoke": "/swe",
      "files": ["src/api.ts", "src/middleware.ts"],
      "reasons": ["TypeScript / JavaScript files"]
    },
    {
      "name": "qa-agent",
      "invoke": "/qa-agent",
      "files": ["tests/api.test.ts"],
      "reasons": ["Test files"]
    }
  ]
}
```

## Workflow

1. Compute the changed file list (`git diff --name-only origin/main`).
2. Run `dispatch-on-change.mjs` to get the agent dispatch plan.
3. Invoke each listed agent on its scoped file set.
4. Agents run in parallel where file sets are disjoint.
5. Coordinator reviews results and merges.

## Customization

Edit `agents/routing.json` to add project-specific routing rules. Rules are
evaluated top-to-bottom; first match wins.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.
