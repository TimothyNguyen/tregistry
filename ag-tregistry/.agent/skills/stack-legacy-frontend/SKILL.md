---
name: stack-legacy-frontend
version: 0.1.1
description: |
  Modernize legacy frontend stacks such as Knockout, YUI, old jQuery widgets,
  and ad hoc browser code toward React/TypeScript.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [migration, swe]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Legacy Frontend

Use for legacy UI migration and strangler-style rewrites.

## References

- `wireapp/wire-webapp` Knockout-to-React migration wiki: migration sequencing reference.
- `yui/yui3`: detection/reference only; do not vendor or extend.
- `reactjs/react-codemod` and `codemod/react-codemod`: codemod patterns.

## Workflow

- Inventory UI frameworks, templates, global state, routing, and browser-only assumptions.
- Keep legacy behavior stable while replacing islands one at a time.
- Prefer native browser APIs and small codemods before new dependencies.
- Preserve accessibility and form semantics during migration.
- Route React/TypeScript implementation details to `stack-react-typescript`.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
