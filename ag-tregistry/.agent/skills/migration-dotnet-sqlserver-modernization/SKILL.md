---
name: migration-dotnet-sqlserver-modernization
version: 0.1.1
description: |
  Plan .NET Framework and SQL Server modernization using compatibility
  assessment, code translation references, and governed data migration lanes.
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

# .NET + SQL Server Modernization

Use for .NET Framework, C#, SQL Server, T-SQL, and legacy Windows service/API
modernization.

## References

- `aws/porting-assistant-dotnet-client`: compatibility assessment patterns.
- `aws/cta`: optional code translation assistance reference.
- `babelfish-for-postgresql/babelfish_compass`: T-SQL compatibility assessment.

## Workflow

- Inventory target frameworks, project files, NuGet packages, IIS/service hosts, and SQL Server objects.
- Separate compile/runtime upgrades from database compatibility work.
- Prefer assessment reports and codemods over hand edits when available.
- Treat generated translation as a draft; require tests and review before landing.
- Gate database reads/writes, schema export, and migration runs through policy and audit.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
