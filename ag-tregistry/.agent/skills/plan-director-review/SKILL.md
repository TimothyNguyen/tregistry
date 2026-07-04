---
name: plan-director-review
version: 0.1.1
description: |
  Director or senior-principal plan review. Reviews scope, sequencing, architecture risk,
  team fit, operational maturity, and executive-readiness before implementation.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [orchestrate, pm]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Director / Senior Principal Review

Use this workflow when a plan needs senior technical leadership review.

## Review Focus

- Is the plan scoped to a clear business and engineering outcome?
- Is the architecture understandable, maintainable, and operable?
- Are the data, security, compliance, and deployment risks explicit?
- Is the work split into reviewable commits and deliverable milestones?
- Are ownership, dependencies, and rollback paths clear?

## Output

Lead with blocking concerns, then material risks, then recommended sequence.
Avoid founder/CEO-style expansion language; this review represents senior
technical leadership in a company environment.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
