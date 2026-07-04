---
name: domain-mlops-databricks
version: 0.1.1
description: |
  Databricks MLOps project structure, model lifecycle, CI/CD, monitoring, and
  governed production ML workflows.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [data]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Databricks MLOps

Use for production ML project structure and model lifecycle work on Databricks.

## References

- `databricks/mlops-stacks`: production ML project structure reference.

## Workflow

- Separate experimentation, feature pipelines, training, deployment, monitoring, and rollback.
- Require data lineage, model evaluation, and approval gates for production promotion.
- Keep metrics and examples aggregate; do not expose raw private datasets.
- Coordinate with `stack-databricks` for bundle/job implementation.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
