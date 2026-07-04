---
name: domain-data-governance
version: 0.1.1
description: |
  Data governance review for classification, lineage, permissions, retention,
  auditability, quality checks, and privacy-safe agent outputs.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [data, pm]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Data Governance

Use for datasets, warehouses, reports, model inputs/outputs, and agent access to
business data.

## Checklist

- Classify data sensitivity and approved purpose.
- Check lineage, owner, retention, permissions, quality gates, and audit trail.
- Prefer summaries and schema metadata over raw records.
- Gate reads, writes, exports, notebook execution, and model output access.
- Redact secrets and private data from events, logs, prompts, and reports.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
