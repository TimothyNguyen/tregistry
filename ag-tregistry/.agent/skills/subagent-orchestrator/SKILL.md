---
name: subagent-orchestrator
version: 0.1.1
description: |
  Plans and materializes local-only subagent manifests for scoped parallel work.
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

# Subagent Orchestrator

Use this skill when a task should be split across planner, explorer,
implementer, test-engineer, reviewer, QA, devtools, docs, or release roles.

## Rules

1. Keep the coordinator in charge of integration and final verification.
2. Give every subagent a narrow role, task, tool list, and allowed path set.
3. Keep egress disabled unless the active profile and policy explicitly allow it.
4. Use write-capable roles only with scoped `allowedPaths`.
5. Do not allow subagents to read credentials, cookies, secret stores, or global
   agent configuration.
6. Subagents must not revert or overwrite work owned by another agent.

## Manifest Shape

```json
{
  "id": "implementer-auth-api",
  "role": "implementer",
  "task": "Add token refresh endpoint",
  "allowedPaths": ["src/auth/**", "tests/auth/**"],
  "disallowedPaths": [".env", "secrets/**"],
  "tools": ["shellRead", "shellWrite", "testExecution"]
}
```

## Local Deployment

Write a plan JSON with an `agents` array, then run:

```bash
npm run subagents:deploy -- path/to/subagents.json <repo>
```

For write-capable implementer/test/docs/release roles that should receive
isolated worktrees:

```bash
npm run subagents:deploy -- path/to/subagents.json <repo> allocate-worktrees
```

This writes repo-local artifacts under:

```text
.architecture-agent/subagents/<agent-id>/manifest.json
.architecture-agent/subagents/<agent-id>/allocation.json
.architecture-agent/subagents/<agent-id>/worktree/
.architecture-agent/subagents/deployment.json
```

## Coordinator Import Or Reject

After a write-capable subagent finishes, inspect and choose:

```bash
npm run subagents:import -- export <agent-id> <repo>
npm run subagents:import -- apply <agent-id> <repo>
npm run subagents:import -- reject <agent-id> <repo> "wrong approach"
```

`apply` checks the patch, enforces `allowedPaths`, and imports changes into the
coordinator worktree. `reject` records a local rejection artifact and leaves the
coordinator worktree unchanged.

## First Roles

Start with:

- `planner`
- `explorer`
- `implementer`
- `test-engineer`
- `reviewer`
- `devtools-agent` only when browser/devtools profile and policy gates are
  active

Defer product browser QA and release automation until the browser and release
policies are explicitly enabled. `devtools-agent` may run local Playwright CLI
smoke checks for buttons, console errors, traces, and screenshots when approved.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
