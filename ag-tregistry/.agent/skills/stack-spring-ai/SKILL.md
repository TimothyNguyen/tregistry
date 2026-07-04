---
name: stack-spring-ai
version: 0.1.1
description: |
  Spring-native AI application patterns using Spring AI and Spring AI examples
  as references, without making them core dependencies.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [swe]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Spring AI

Use for Spring applications that integrate model calls, tools, vector stores, or
AI workflows.

## References

- `spring-projects/spring-ai`: Spring-native AI app patterns.
- `spring-projects/spring-ai-examples`: implementation references.

## Workflow

- Keep model/provider configuration externalized and environment-specific.
- Gate network/model calls by policy; no default public egress.
- Treat examples as reference implementations, not production defaults.
- Require tests around prompt/tool contracts and failure behavior.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
