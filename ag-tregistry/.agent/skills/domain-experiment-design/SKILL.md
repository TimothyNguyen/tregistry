---
name: domain-experiment-design
version: 0.1.1
description: |
  Experiment design review for randomization, power, metrics, guardrails,
  exposure, analysis plans, and rollout risk.
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

# Experiment Design

Use for A/B tests, randomized experiments, holdouts, feature rollouts, and
measurement plans.

## Checklist

- Define hypothesis, unit of randomization, target population, exposure, primary
  metric, guardrails, and stopping rules.
- Check sample size, power, seasonality, interference, novelty effects, and
  instrumentation risk.
- Separate exploratory metrics from decision metrics.
- Require pre-analysis plan for high-stakes decisions.
- Do not recommend launch decisions without validity checks.

## Privacy

- Keep outputs aggregate and avoid user-level event dumps.
- Gate data reads and warehouse queries by policy.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
