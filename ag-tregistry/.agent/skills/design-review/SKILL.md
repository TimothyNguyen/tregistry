---
name: design-review
version: 0.1.1
description: |
  Reviews product UI and interaction quality for practical design issues.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [design-agent, swe, qa-agent]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Design Review

Reviews product UI and interaction quality for practical design issues.

## Steps

1. Confirm the user goal and scope.
2. Read the relevant local project files.
3. If the user wants design-file context, choose one approved MCP option:
   - Figma MCP: official Figma MCP option at
     `https://github.com/mcp/com.figma.mcp/mcp`. Use only when `figmaMcp`
     module and `figmaMcp` tool are policy-approved for the active session.
   - OpenPencil MCP: open-source design editor option using `@open-pencil/mcp`
     and `openpencil-mcp`. Use when `openPencilMcp` module and
     `openPencilMcp` tool are policy-approved. MCP clients should allow
     `mcp__open-pencil__*` only for this scoped design work.
4. Check policy requirements before any privileged action.
5. Produce a concise result with evidence, risks, and next actions.

## Design MCP Options

Prefer local project files and screenshots first. Use design MCP only when the
user asks for live design-file context or design editing.

| Option | Use When | Setup Hint | Default Posture |
|---|---|---|---|
| Figma MCP | Existing Figma/FigJam/Figma Make files are source of truth. | `https://github.com/mcp/com.figma.mcp/mcp` | Approval-required egress and writes. |
| OpenPencil MCP | Open-source/local design workflow or `.fig`/`.pen` files are source of truth. | `npm install -g @open-pencil/mcp` then run `openpencil-mcp`; allow `mcp__open-pencil__*` in approved MCP clients. | Approval-required egress and writes. |

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
