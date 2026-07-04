---
name: stack-aws
version: 0.1.1
description: |
  AWS application modernization planning with least-privilege, local-first
  validation, explicit approvals, and no default cloud mutation.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [cloud]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# AWS Stack

Use for AWS-hosted services, migration plans, infrastructure references, and
deployment readiness.

## Workflow

- Inventory local IaC, service manifests, SDK usage, IAM assumptions, logs, and
  deployment scripts before touching cloud accounts.
- Prefer static/local validation over live AWS calls.
- Require approval for account discovery, deploys, DMS tasks, endpoint creation,
  IAM changes, secret reads, and data access.
- Never print credentials, account secrets, private customer data, or full logs
  into outputs or audit payloads.

## Routes

- Database migration: `stack-aws-dms`.
- Spring services: `stack-spring-boot`.
- Databricks workloads: `stack-databricks`.
- Security/governance: `security-review`.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
