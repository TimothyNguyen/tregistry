---
name: investigate
version: 0.1.1
description: |
  Root-cause investigation workflow for bugs, failing tests, broken integrations, and unexpected behavior.
  Investigates before proposing fixes and records evidence for each hypothesis.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [swe, qa-agent, security]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Investigate

Use this workflow when something is broken or unclear.

## Steps

1. Reproduce or characterize the failure.
2. Identify the expected behavior.
3. Trace the smallest relevant code/data path.
4. Form one hypothesis at a time.
5. Test each hypothesis with focused evidence.
6. Propose a fix only after the likely root cause is identified.
7. Add or recommend a regression check.

## Stop Conditions

- Stop and report when required data or credentials are unavailable.
- Stop and ask before running policy-gated write actions.
- Stop after repeated failed fix attempts and summarize what was disproven.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
