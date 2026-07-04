---
name: plan-pm-review
version: 0.1.1
description: |
  Product manager plan review. Reviews user value, requirements clarity, acceptance
  criteria, rollout, measurement, stakeholder impact, and non-goals.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [pm, spec-agent]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# PM Review

Use this workflow when a plan needs product management review before engineering
execution.

## Review Focus

- What user or business problem does this solve?
- Are requirements and non-goals explicit?
- Are acceptance criteria testable?
- Are rollout, adoption, support, and measurement plans clear?
- Are stakeholder impacts and dependencies identified?
- Are analytics or experiment metrics defined without overclaiming causality?

## Output

Report missing requirements, ambiguous acceptance criteria, product risks,
measurement gaps, and recommended scope adjustments.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
