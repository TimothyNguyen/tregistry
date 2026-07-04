---
name: health
version: 0.1.1
description: |
  Enterprise-safe code health dashboard. Detects and runs approved local quality checks
  such as type checks, lint, tests, dependency checks, dead-code checks, and shell lint.
  Produces a read-only scorecard and recommendations.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [swe, qa-agent, cloud, security]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Health

Use this workflow for code quality dashboards, health checks, or "run all
checks" requests.

## Hard Gate

Do not fix issues in this workflow. Produce a dashboard, evidence, and
recommendations only. The user decides what to change.

## Step 1: Detect Health Stack

Prefer project-declared tools. Look for:

- `package.json` scripts: `typecheck`, `lint`, `test`, `test:e2e`, `knip`
- `tsconfig.json`
- `eslint.config.*`, `.eslintrc*`, `biome.json`, `biome.jsonc`
- `pyproject.toml`, `pytest.ini`, `ruff.toml`
- `pom.xml`, `build.gradle`, `gradlew`
- `.csproj`, `.sln`, `global.json`
- `go.mod`, `Cargo.toml`
- shell scripts under `scripts/` or `bin/`

If the project has a profile-declared health stack, use it exactly.

## Step 2: Run Read-Only Checks

Run checks sequentially. Record command, exit code, duration, and the last
relevant output lines.

Candidate categories:

| Category | Examples |
|---|---|
| Type check | `tsc --noEmit`, `mypy`, `dotnet build --no-restore`, `mvn test -DskipTests` |
| Lint | `eslint`, `biome check`, `ruff check`, `dotnet format --verify-no-changes` |
| Unit tests | `npm test`, `pytest`, `mvn test`, `dotnet test` |
| UI tests | Playwright or Selenium, only when policy enables browser automation |
| Data tests | dbt tests, SQL checks, Databricks job tests, approved local fixtures |
| Dead code | `knip`, project-specific unused-code checks |
| Security | dependency audit or static checks approved by policy |
| Shell lint | `shellcheck` |

Skipped tools are not failures. Mark them `SKIPPED` with a reason.

## Step 3: Score

Score each detected category from 0 to 10:

| Score | Meaning |
|---|---|
| 10 | Clean |
| 7-9 | Warnings or minor issues |
| 4-6 | Significant issues |
| 0-3 | Broken or high-risk |

Suggested weights:

- Tests: 28%
- Type check/build: 22%
- Lint/static analysis: 18%
- Security/dependency checks: 12%
- Dead code: 10%
- Shell/script hygiene: 5%
- Documentation/config sanity: 5%

Redistribute skipped category weights across detected categories.

## Step 4: Dashboard

Report:

- Project and branch.
- Detected tools.
- Per-category status, score, duration, and summary.
- Composite score.
- Top regressions or risks.
- Highest-impact recommendations.

## Step 5: Local History

If policy allows local audit/history writes, append one JSONL event under the
project-local state directory. Do not write to a global user directory by
default.

The event must not include secrets, full prompts, full file contents, raw
customer data, raw campaign data, or raw query results.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
