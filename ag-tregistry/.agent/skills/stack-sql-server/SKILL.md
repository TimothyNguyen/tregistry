---
name: stack-sql-server
version: 0.1.1
description: |
  SQL Server schema, T-SQL, stored procedure, job, and application data-access
  modernization with governed database access.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [swe, migration]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# SQL Server Stack

Use for SQL Server schemas, stored procedures, T-SQL, jobs, migration readiness,
and application data-access code.

## Workflow

- Inventory schemas, procedures, functions, jobs, linked servers, permissions,
  and application query paths from repo-local artifacts first.
- Require approval for live database reads, exports, writes, and migration runs.
- Avoid raw row dumps; report aggregates, schema facts, and narrow examples.
- Use compatibility assessment before porting to Postgres.

## Routes

- .NET modernization: `migration-dotnet-sqlserver-modernization`.
- Postgres migration: `stack-sqlserver-to-postgres`.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
