---
name: release
version: 0.1.1
description: |
  Policy-gated release preparation workflow. Checks readiness, tests, docs, risk, and rollback
  before handoff to human-approved merge or deploy steps.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [pm, cloud, release-agent]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Release

Use this workflow before merge, deploy, or production handoff.

## Steps

1. Confirm the change scope and commit sequence.
2. Verify tests and documented manual checks.
3. Check security, data, migration, and operational risks.
4. Confirm docs or release notes are updated when needed.
5. Identify rollback plan and owner.
6. Request approval before any git write, deployment, or external system action.

## Release Gates

- Tests pass or failures are explained.
- Policy-gated actions are approved.
- Data changes have rollback or repair path.
- User-facing changes have QA evidence.
- Security findings are resolved or explicitly accepted.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
