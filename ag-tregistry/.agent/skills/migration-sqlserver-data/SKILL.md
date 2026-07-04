---
name: migration-sqlserver-data
version: 0.1.0
description: |
  Execute data migration from SQL Server to Postgres.
  Validates data integrity with checksums and row counts.
agents: [migration-engineer, swe]
allowed-tools: [Read, Bash, Grep]

metadata:
  category: "infrastructure"
  domain: "data-migration"
  tier: "essential"
  support:
    maintenance-status: "active"
    owner-team: "data-engineering"
    last-reviewed: "2026-06-26"
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# SQL Server Data Migration

Execute data migration from SQL Server to Postgres with validation.

## Workflow

1. Connect to SQL Server and PostgreSQL
2. Export data from SQL Server
3. Transform and load into PostgreSQL
4. Validate data integrity (checksums, row counts)
5. Handle constraints and sequences
6. Output migration log

## Checklist

- [ ] Validate source and target databases
- [ ] Plan data migration (order of tables, constraints)
- [ ] Extract data from SQL Server
- [ ] Transform data (type conversions, encodings)
- [ ] Load data into PostgreSQL
- [ ] Validate checksums and row counts
- [ ] Handle sequences and identity columns

## When to Use

Use after `/migration-sqlserver-schema` to migrate actual data.

## Related Skills

- `/migration-engineer` — Overall coordination
- `/migration-sqlserver-schema` — Schema conversion phase
- `/migration-sqlserver-test` — Validation phase
