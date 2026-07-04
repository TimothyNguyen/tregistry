---
name: guard
version: 0.1.1
description: |
  Applies stricter local safety posture for risky tools and filesystem boundaries.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [swe, migration, cloud, _infrastructure, security]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Guard

Applies stricter local safety posture for risky tools and filesystem boundaries.

## Steps

1. Confirm the user goal and scope.
2. Read the relevant local project files.
3. Check policy requirements before any privileged action.
4. Produce a concise result with evidence, risks, and next actions.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
