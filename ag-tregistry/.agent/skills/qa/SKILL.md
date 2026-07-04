---
name: qa
version: 0.1.1
description: |
  Enterprise-safe QA workflow. Plans and verifies user-facing or service behavior using
  local tests and approved tools. Browser automation is optional and disabled by default.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [qa-agent, swe]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# QA

Use this workflow to verify a feature, bug fix, or release candidate.

## Steps

1. Identify the behavior under test.
2. List the smallest useful verification path.
3. Prefer local tests and deterministic fixtures.
4. Use browser automation only when the active policy enables it.
5. Record bugs with reproduction steps and expected behavior.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
