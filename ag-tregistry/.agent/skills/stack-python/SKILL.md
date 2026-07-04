---
name: stack-python
version: 0.1.1
description: |
  Python service, library, and data workflow modernization with minimal
  dependencies, local tests, packaging hygiene, and privacy-safe execution.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [swe, data]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Python Stack

Use for Python packages, services, scripts, CLIs, data jobs, and test suites.

## Workflow

- Inventory `pyproject.toml`, lock files, entry points, test runners, notebooks,
  generated code, and runtime environment.
- Prefer standard library and existing dependencies before adding packages.
- Keep local checks small and reproducible.
- Gate network calls, credential reads, database access, and model/API calls.
- Do not log raw datasets, secrets, prompts with secrets, or full file contents.

## Checks

- Run the smallest relevant test first.
- Use static import/package checks for packaging changes.
- Add one focused regression check for non-trivial logic.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
