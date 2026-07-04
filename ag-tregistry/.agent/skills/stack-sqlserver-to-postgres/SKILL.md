---
name: stack-sqlserver-to-postgres
version: 0.1.1
description: |
  SQL Server to Postgres migration planning with T-SQL compatibility checks,
  pgloader experiments, and production cutover guardrails.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [migration]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# SQL Server to Postgres

Use for schema, query, and data migration from SQL Server to Postgres.

## References

- `babelfish-for-postgresql/babelfish_compass`: T-SQL compatibility assessment.
- `dimitri/pgloader`: local experiment/data-copy reference.
- `aws-samples/aws-database-migration-samples`: DMS/SCT lab patterns.

## Workflow

- Inventory schema objects, stored procedures, functions, jobs, data volumes, and application query paths.
- Run compatibility assessment before rewriting SQL.
- Separate local migration experiments from production cutover.
- Require rollback, reconciliation, and performance validation plans.
- Gate all database access through policy and audit.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
