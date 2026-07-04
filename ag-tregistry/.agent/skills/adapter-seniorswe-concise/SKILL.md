---
name: adapter-seniorswe-concise
version: 0.1.1
description: |
  Optional Seniorswe-Concise hook and MCP adapter for YAGNI mode injection across
  Claude, Codex, Copilot, and MCP hosts.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [swe, _infrastructure]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Seniorswe-Concise Adapter

Use when installing, testing, or modifying Seniorswe-Concise hook/MCP integration.

## Runtime

- Hook code lives in `adapters/seniorswe-concise/hooks`.
- MCP code lives in `adapters/seniorswe-concise/mcp`.
- State defaults to `.architecture-agent/state/seniorswe-concise`.
- Config defaults to `.architecture-agent/seniorswe-concise/config.json`.

## Rules

- Keep Seniorswe-Concise adapter optional; core skills remain plain Markdown.
- Do not mutate global host config unless the user/admin explicitly chooses that install target.
- Keep the MCP server closed-world and instruction-only.
- Run `npm test -- tests/seniorswe-concise-adapter.test.mjs` after changes.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
