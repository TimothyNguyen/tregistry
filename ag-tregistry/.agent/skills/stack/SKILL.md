---
name: stack
version: 0.1.1
description: |
  Tech stack meta-loader. Auto-detects project tech stack from repo signals and
  loads the matching stack-* skill. User can override detection explicitly.
  Invoke via /stack, or when the user says "load stack", "detect stack",
  "set stack to X", or any stack-* skill needs context.
argument-hint: "[aws|postgres|python|react|spring|csharp|databricks|sql-server|legacy]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [_infrastructure, swe]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Stack Meta-Loader

Detect the project tech stack from file system signals, then load the matching
`stack-*` skill. User can override detection at any time.

## Auto-detection order

| Signal | Stack skill loaded |
|---|---|
| `package.json` with `react` or `@types/react` dep | `stack-react-typescript` |
| `pyproject.toml` or `setup.py` | `stack-python` |
| `pom.xml` or `build.gradle` + Spring dependency | `stack-spring-boot` |
| Spring AI dependency | `stack-spring-ai` |
| `*.csproj` or `*.sln` | `stack-csharp` |
| `databricks.yml` | `stack-databricks` |
| `dbt_project.yml` | `stack-databricks-dbt` |
| `*.tf` or `cdk.json` or `serverless.yml` | `stack-aws` |
| `schema.sql` / `*.sql` with `SERIAL` or `$$` | `stack-postgres` |
| `schema.sql` / `*.sql` with `GO` or `EXEC sp_` | `stack-sql-server` |

Detection runs top-to-bottom. Multiple stacks can load simultaneously
(e.g. React + Postgres is common).

## Explicit overrides

```
/stack aws           → loads stack-aws
/stack postgres      → loads stack-postgres
/stack python        → loads stack-python
/stack react         → loads stack-react-typescript
/stack spring        → loads stack-spring-boot
/stack csharp        → loads stack-csharp
/stack databricks    → loads stack-databricks
/stack dbt           → loads stack-databricks-dbt
/stack sql-server    → loads stack-sql-server
/stack dms           → loads stack-aws-dms
/stack legacy        → loads stack-legacy-frontend
```

## What "loading" means

Prepend the matching `stack-*` skill's context into the current session.
Do not unload the base agent skill — stack context is additive.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.
