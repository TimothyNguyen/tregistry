---
name: migration-sqlserver-test
version: 0.1.0
description: |
  Validate migrated data matches source.
  Tests correctness, constraints, and triggers.
agents: [migration-engineer, qa-agent]
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

# SQL Server Data Testing

Validate migrated data correctness and test all constraints.

## Workflow

1. Compare row counts (source vs. target)
2. Validate data values (sample checks)
3. Test constraints (primary keys, foreign keys, unique)
4. Verify triggers and views
5. Output test report and sign-off

## Checklist

- [ ] Compare row counts across all tables
- [ ] Validate key data values (spot checks)
- [ ] Verify primary key integrity
- [ ] Verify foreign key relationships
- [ ] Test views and computed columns
- [ ] Validate triggers work correctly
- [ ] Check constraint violations
- [ ] Output test report

## When to Use

Use after `/migration-sqlserver-data` to validate correctness.

## Related Skills

- `/migration-engineer` — Overall coordination
- `/migration-sqlserver-data` — Data migration phase
- `/migration-sqlserver-perf` — Performance phase
