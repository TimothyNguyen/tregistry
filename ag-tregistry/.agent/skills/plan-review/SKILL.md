---
name: plan-review
version: 0.1.1
description: |
  Enterprise-safe plan review workflow. Reviews a proposed implementation plan for scope,
  architecture, testability, policy compliance, data risk, and delivery sequencing before code changes begin.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [swe, qa-agent, spec-agent, orchestrate]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Plan Review

Use this workflow before implementation when a user has a design, spec, task
list, or architecture plan that needs review.

## Steps

1. Identify the plan's goal and intended behavioral change.
2. Check whether the plan is scoped to one deliverable or should be split.
3. Review architecture boundaries, data flow, policy gates, and test strategy.
4. Flag missing dependencies, hidden state, rollout risk, and unclear ownership.
5. Recommend a commit sequence where each commit changes one behavior surface.

## Review Lanes

- Product fit and scope.
- Engineering architecture.
- Data and governance risk.
- Testability and verification.
- Developer experience.
- Release and rollback.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
