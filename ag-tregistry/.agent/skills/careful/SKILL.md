---
name: careful
version: 0.1.1
description: |
  Destructive command guardrails. Warns before rm -rf, DROP TABLE, force-push,
  git reset --hard, kubectl delete, and similar operations. Use when touching
  production, shared environments, or when explicitly asked to use safety mode.
allowed-tools:
  - Read
  - Bash
agents: [migration, cloud, _infrastructure, security, release-agent]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Careful — Destructive Command Guardrails

Safety mode is **active**. Before running any destructive bash command, warn the
user and describe what will be lost. Let the user confirm before proceeding.

## Protected patterns

| Pattern | Example | Risk |
|---|---|---|
| `rm -rf` / `rm -r` / `rm --recursive` | `rm -rf /var/data` | Recursive delete |
| `DROP TABLE` / `DROP DATABASE` | `DROP TABLE users;` | Data loss |
| `TRUNCATE` | `TRUNCATE orders;` | Data loss |
| `git push --force` / `-f` | `git push -f origin main` | History rewrite |
| `git reset --hard` | `git reset --hard HEAD~3` | Uncommitted work loss |
| `git checkout .` / `git restore .` | `git checkout .` | Uncommitted work loss |
| `kubectl delete` | `kubectl delete pod` | Production impact |
| `docker rm -f` / `docker system prune` | `docker system prune -a` | Container/image loss |

## Safe exceptions

These are allowed without warning:

- `rm -rf node_modules` / `.next` / `dist` / `__pycache__` / `.cache` / `build` / `.turbo` / `coverage`

## Behavior

For every bash command, check before running:

1. Does the command match a protected pattern above?
2. Is it a safe exception?
3. If destructive and not excepted: warn the user with the specific risk, then ask to confirm.
4. If the user confirms: proceed.
5. If the user cancels: stop and explain what alternative achieves the goal safely.

Never run a protected command silently. Always surface the risk first.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
