---
name: migration-sqlserver-schema
version: 0.1.0
description: |
  Convert SQL Server T-SQL DDL to PostgreSQL schema.
  Handles incompatibilities: CLR → functions, XML → JSONB, spatial types.
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

# SQL Server Schema Conversion

Convert T-SQL DDL to PostgreSQL schema.

## Workflow

1. Analyze SQL Server schema
2. Convert tables, views, stored procedures
3. Handle incompatibilities (CLR, XML, spatial)
4. Generate PostgreSQL DDL
5. Validate converted schema

## Checklist

- [ ] Extract SQL Server DDL (tables, views, procedures)
- [ ] Identify incompatibilities
- [ ] Convert T-SQL to PostgreSQL syntax
- [ ] Handle special types (XML → JSONB, spatial → PostGIS)
- [ ] Generate and validate PostgreSQL DDL
- [ ] Output conversion report

## When to Use

Use after `/migration-sqlserver-assess` to convert schema.

## Related Skills

- `/migration-engineer` — Overall coordination
- `/migration-sqlserver-assess` — Assessment phase
- `/migration-sqlserver-data` — Data migration phase
