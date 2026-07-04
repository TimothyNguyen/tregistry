---
name: adapter-google-adk
version: 0.1.1
description: |
  Optional Google ADK host adapter boundary for invoking skills and tools
  without making core architecture depend on ADK runtime packages.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [orchestrate, _infrastructure, cloud]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Google ADK Adapter

Use when designing or reviewing Google ADK integration.

## Contract

- Keep ADK optional and host-side.
- Transform generated skills into ADK instructions declaratively where possible.
- Gate network/model/tool calls by policy.
- Keep telemetry disabled unless an internal, approved endpoint is configured.
- Do not store prompts, secrets, or tool outputs in third-party telemetry.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
