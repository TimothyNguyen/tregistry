---
name: autoplan
version: 0.1.2
description: |
  Runs the plan review pipeline before coding begins, then a post-implementation critic gate before surfacing results.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [swe, orchestrate, spec-agent]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Autoplan

Runs the plan review pipeline before coding begins and a post-implementation critic gate before surfacing results to the user.

## Phase 1 — Pre-Implementation Plan Review

1. Confirm the user goal and scope.
2. Read the relevant local project files.
3. Run the plan review pipeline: invoke `plan-eng-review`, `plan-director-review`, and any relevant domain or design reviews.
4. Revise the plan based on review findings.
5. Confirm the reviewed plan with the user before proceeding to implementation.

## Phase 2 — Implementation

6. Implement the reviewed plan using the appropriate role agents (`/swe`, `/data`, `/cloud`, or `/migration`).
7. Commit after each discrete behavior change.

## Phase 3 — Post-Implementation Critic Gate

After implementation and before surfacing results to the user:

8. Run `security-review` — check for credential exposure, unsafe tool access, and policy violations.
9. Run `seniorswe-concise-review` — check for over-engineering, unnecessary dependencies, and YAGNI violations.
10. Run `qa` — verify that tests exist, pass, and cover the changed behavior.
11. Collect critic findings. If any critic finds a blocking issue, return to Phase 2 to fix it.
12. Surface a final summary: reviewed plan, implementation diff, critic results, and any deferred items.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Critic Gate Rules

- A blocking finding from `security-review` must be resolved before surfacing results.
- A blocking finding from `seniorswe-concise-review` should be resolved unless the user explicitly accepts the debt.
- Test failures from `qa` block surfacing results.
- Non-blocking `seniorswe-concise-review` findings may be recorded as `seniorswe-concise:` debt comments in place of immediate fixes.
- Skip the critic gate only when the user explicitly requests `--no-critic` or the active profile disables it.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
