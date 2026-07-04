---
name: adapter-mcp
version: 0.1.1
description: |
  Design optional Model Context Protocol adapters with default-deny tools,
  narrow schemas, and local audit boundaries.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [swe, _infrastructure, orchestrate, cloud]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# MCP Adapter

Use when adding or reviewing an MCP server/client integration.

## References

- `modelcontextprotocol/servers`: server pattern reference.
- Existing local adapter: `adapters/ponytail/mcp`.

## Rules

- Keep MCP optional; core skills must work without it.
- Default tools to read-only and closed-world where possible.
- Use narrow schemas and explicit annotations.
- Gate credentials, writes, network egress, and privileged tools by policy.
- Add tests for instruction builders separately from SDK startup.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
