---
name: documentation
version: 0.1.1
description: |
  Documentation workflow for generating, updating, and reviewing project docs after implementation.
  Focuses on accurate code-backed docs without public browsing or telemetry.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [qa-agent, pm, spec-agent]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Documentation

Use this workflow to create or update docs from local project evidence.

## Steps

1. Identify the target audience and documentation type.
2. Read the relevant local code, tests, config, and existing docs.
3. Write docs that match the implementation.
4. Remove stale or contradictory claims.
5. Include setup, usage, verification, and operational notes when relevant.

## Documentation Types

- Reference.
- How-to.
- Tutorial.
- Explanation.
- Release notes.
- Architecture decision notes.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
