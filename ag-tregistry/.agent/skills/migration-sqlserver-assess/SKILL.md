---
name: migration-sqlserver-assess
version: 0.1.0
description: |
  Assess SQL Server database for Postgres migration readiness.
  Analyzes schema, special features, data volume, and incompatibilities.
agents: [migration-engineer, swe]
allowed-tools: [Read, Bash, Grep]

metadata:
  category: "infrastructure"
  domain: "data-migration"
  tier: "essential"
  dependencies:
    mcps: []
    skills: []
  approval-gates:
    policy-required: []
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

# SQL Server Assessment

Analyze SQL Server database for Postgres migration readiness.

## Role

Gather baseline information about the SQL Server instance and database before migration planning. This skill is the first phase of the migration workflow.

## Workflow

1. **Connect to SQL Server**
   - What SQL Server version? (2012, 2016, 2019, 2022)
   - How to access? (connection string, credentials, firewall)
   - Database name and owner

2. **Scan Schema**
   - How many tables? Views? Stored procedures?
   - What's the total data volume? (rows, size in GB)
   - Are there special types? (XML, spatial, hierarchyid)

3. **Identify Incompatibilities**
   - ❌ CLR assemblies → Must convert to PostgreSQL functions
   - ❌ Service Broker → Must redesign with PostgreSQL messaging
   - ❌ Full-text search → Must reindex with PostgreSQL FTS
   - ❌ XML columns → Must convert to JSONB or text
   - ❌ Spatial types → PostGIS required
   - ❌ Encrypted columns → Decryption/re-encryption needed

4. **Measure Data Complexity**
   - How many foreign key relationships?
   - Are there circular dependencies?
   - Custom types? Sequences?
   - Triggers? (count and purpose)

5. **Output Assessment Report**
   - Compatibility score (Green/Yellow/Red)
   - Effort estimate (hours)
   - Risk factors
   - Recommended approach

## Checklist

- [ ] Connect to SQL Server
- [ ] Query schema information (tables, columns, types)
- [ ] Identify special features (CLR, Service Broker, FTS)
- [ ] Measure data volume and complexity
- [ ] Identify incompatibilities
- [ ] Output assessment report with recommendations

## Questions to Answer

**About the SQL Server instance:**
- What version? (2012, 2016, 2019, 2022, or Azure SQL?)
- How many databases are we migrating?
- Total storage used? Peak concurrent users?

**About the target database:**
- How many tables? Approximate row counts?
- Any specialized types? (XML, spatial, CLR)
- Stored procedures? Triggers? Views?
- Full-text search enabled?

**About constraints & relationships:**
- Primary keys on all tables?
- Foreign key constraints? (count)
- Circular dependencies?
- Sequences or identity columns?

**About the migration context:**
- Timeline? (weeks? months?)
- Downtime tolerance? (minutes? hours?)
- Budget constraints?
- Team experience with PostgreSQL?

## Anti-Patterns

❌ **"Let's just migrate without assessing"** → Leads to surprises (incompatibilities, performance issues)
❌ **"I'll assess manually and take notes"** → Assessment should be automated and repeatable
❌ **"This database looks simple"** → Even simple databases can have hidden complexity (triggers, CLR, etc.)

## Output Format

**Assessment Report**

```
SQL Server Migration Assessment
================================

Database: [name]
Server: [instance] (version [version])
Date: [date]

COMPATIBILITY SCORE: [Green/Yellow/Red]

SCHEMA OVERVIEW
- Tables: N
- Views: N
- Stored Procedures: N
- Total Data Size: N GB
- Total Rows: N

INCOMPATIBILITIES FOUND
- CLR Assemblies: [Y/N] (effort: [hours])
- Service Broker: [Y/N]
- Full-Text Search: [Y/N]
- XML Columns: [Y/N]
- Spatial Data: [Y/N]

COMPLEXITY FACTORS
- Foreign Keys: N
- Circular Dependencies: [Y/N]
- Sequences: N
- Triggers: N

EFFORT ESTIMATE: [hours] hours
RISK LEVEL: [Low/Medium/High]

RECOMMENDATIONS
1. [action]
2. [action]
```

## Examples

### Example 1: Small Database (< 100GB)

**Input:** 42 tables, 2.3B rows, T-SQL stored procedures, basic schema
**Assessment:** Green (low complexity)
**Effort:** 40 hours
**Output:** Clean migration path, no special handling needed

### Example 2: Complex Database (100GB+)

**Input:** 200 tables, 50B rows, CLR assemblies, Service Broker, FTS, XML columns
**Assessment:** Red (high complexity)
**Effort:** 200 hours
**Output:** Requires phased approach, multiple iterations, expert review

### Example 3: Medium Database with Specialization

**Input:** 80 tables, 5B rows, spatial data (PostGIS), encrypted columns, triggers
**Assessment:** Yellow (medium complexity)
**Effort:** 80 hours
**Output:** Standard migration + PostGIS setup + decryption strategy needed

## When to Use

Use `/migration-sqlserver-assess` when:
- Planning SQL Server → Postgres migration
- Need baseline data before architecture review
- Assessing migration effort and risk
- Identifying blocking incompatibilities
- First step in migration workflow

## Related Skills

- `/migration-engineer` — Overall migration coordination
- `/migration-sqlserver-schema` — Convert schema after assessment
- `/migration-review` — Architecture review
- `/careful` — Deployment safety checks
