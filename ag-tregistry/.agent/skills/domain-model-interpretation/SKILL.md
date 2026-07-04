---
name: domain-model-interpretation
version: 0.1.1
description: |
  Model interpretation review for feature effects, calibration, drift,
  uncertainty, explanation limits, and decision-risk communication.
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

# Model Interpretation

Use for model explanation, feature importance, partial dependence, SHAP-style
summaries, calibration, drift, and recommendation risk.

## Checklist

- Identify model purpose, decision surface, training data window, and target.
- Check calibration, drift, subgroup behavior, leakage, and explanation
  stability.
- Treat explanations as approximations; do not overclaim causality.
- Require human review for high-impact recommendations.
- Keep examples aggregate or synthetic unless policy approves data access.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
