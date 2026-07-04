---
name: adapter-openapi
version: 0.1.1
description: |
  Use OpenAPI contracts and optional generated clients/servers while keeping
  generated code isolated and reviewed.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [swe, spec-agent]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# OpenAPI Adapter

Use for API contract generation, client/server stubs, and compatibility checks.

## References

- `OpenAPITools/openapi-generator`: generator reference.

## Rules

- Treat generated code as an adapter boundary, not hand-edited core.
- Pin generator version and config in project files.
- Review generated diffs for breaking API changes.
- Require tests around at least one request/response path for changed contracts.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
