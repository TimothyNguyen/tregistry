---
name: ship
version: 0.1.2
description: |
  Prepares a human-approved PR, merge, or release handoff. Runs parallel specialist
  review (QA, security, PM, DevEx) before producing the handoff artifact.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [swe, cloud, release-agent]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Ship

Prepares a human-approved PR, merge, or release handoff.

## Phase 1: Confirm Scope

1. Confirm the user goal: what is being shipped, to where, and who approves.
2. Read relevant local project files: changelogs, migrations, config diffs.
3. Check policy requirements before any privileged action.

## Phase 2: Parallel Specialist Review

Before handoff, apply four specialist lenses. Treat each as an independent review — collect all findings before proceeding to Phase 3.

### QA Lens
- Are all acceptance criteria covered by tests?
- Is test coverage adequate for the changed paths?
- Are there regression risks in adjacent unchanged code?
- See `references/test-quality.md` for test quality signals.

### Security Lens
- Does the diff touch auth, credentials, data access, or agent tools?
- Are OWASP LLM Top 10 risks addressed for any LLM/agent code?
- Any new public egress, public endpoint, or privilege escalation?
- See `references/security-checklist.md` for the full checklist.

### PM / Stakeholder Lens
- Does the change match the spec? No undocumented behavior changes?
- Are breaking changes called out in the changelog?
- Is there anything a non-technical stakeholder needs to act on?

### DevEx Lens
- Does the diff introduce friction for the next engineer? (Dead code, magic numbers, missing types)
- Are error messages actionable?
- Is the commit history clean and atomic?

## Phase 3: Consolidate and Ship

1. Collect findings from all four lenses.
2. For any **Critical** finding: block ship, fix it first.
3. For any **Important** finding: document in PR description, assign follow-up.
4. For **Minor** findings: note in PR description.
5. Produce the handoff artifact with:
   - Summary of what changed and why
   - Findings from specialist review with severity
   - Explicit approval request from the human

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
