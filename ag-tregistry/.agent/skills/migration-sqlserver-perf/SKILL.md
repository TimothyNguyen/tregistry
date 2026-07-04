---
name: migration-sqlserver-perf
version: 0.1.0
description: |
  Performance tune PostgreSQL after migration.
  Creates indexes, analyzes queries, establishes baselines.
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

# SQL Server Performance Tuning

Performance tune PostgreSQL after migration.

## Workflow

1. Analyze existing indexes
2. Create indexes on primary and foreign keys
3. Collect table statistics (ANALYZE)
4. Benchmark query performance
5. Tune PostgreSQL settings (buffer pool, cache)
6. Establish performance baseline
7. Output baseline metrics and recommendations

## Checklist

- [ ] Verify existing indexes were created
- [ ] Add indexes on primary/foreign keys
- [ ] Run ANALYZE on all tables
- [ ] Identify slow queries
- [ ] Benchmark key operations
- [ ] Tune PostgreSQL settings
- [ ] Establish performance baseline
- [ ] Output baseline metrics and tuning report

## When to Use

Use after `/migration-sqlserver-test` to optimize performance.

## Related Skills

- `/migration-engineer` — Overall coordination
- `/migration-sqlserver-test` — Testing phase
- `/careful` — Deployment safety checks
