---
name: stack-react-typescript
version: 0.1.1
description: |
  React and TypeScript application modernization, including codemods, Redux
  Toolkit patterns, RTK Query, and UI migration checks.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [swe, design-agent]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# React + TypeScript

Use for React upgrades, TypeScript migrations, Redux modernization, and client
contract work.

## References

- `reactjs/react-codemod` / `codemod/react-codemod`: React migration codemods.
- `reduxjs/redux-toolkit`: Redux Toolkit and RTK Query baseline patterns.
- `OpenAPITools/openapi-generator`: optional generated client/server contracts.

## Workflow

- Inventory React version, router, bundler, state management, test runner, and generated clients.
- Use codemods for mechanical React changes, then review manually.
- Prefer Redux Toolkit slices and RTK Query only when app state complexity justifies them.
- Keep generated OpenAPI clients isolated behind a small project boundary.
- Verify rendering, accessibility basics, and representative user flows.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
