---
name: doubt-driven-development
version: 0.1.0
description: |
  Challenge assumptions before and during implementation. Surface load-bearing doubts
  early so they can be resolved with evidence rather than discovered as bugs.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [swe, qa-agent, spec-agent]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Doubt-Driven Development

Before implementing, surface and challenge assumptions. A doubt raised now is cheaper than a bug found in review.

## When to Use

Invoke when:
- Starting a task with unclear requirements
- The implementation path has multiple plausible interpretations
- A past assumption turned out to be wrong in this codebase
- The reviewer is likely to ask "did you consider X?"

## The Process

### Step 1: List Assumptions

Before writing any code, list every assumption the implementation depends on. One line each:

```
1. The user ID is always a UUID string, never an integer.
2. The API returns 404 (not 200 with empty body) when the resource is missing.
3. Concurrent calls to this function are not possible in the current usage.
4. The config file is always present at startup.
```

### Step 2: Rate Each Assumption

For each assumption, rate confidence and blast radius if wrong:

| # | Assumption | Confidence | Blast Radius if Wrong |
|---|------------|------------|----------------------|
| 1 | User ID is UUID string | High — seen in 12 call sites | Low — easy type fix |
| 2 | API returns 404 for missing | Medium — only tested in staging | High — silent data loss |
| 3 | No concurrent calls | Low — no lock in caller | High — race condition |
| 4 | Config always present | High — startup guard exists | Low — hard crash on start |

### Step 3: Surface Load-Bearing Doubts

Any assumption with **Low confidence AND High blast radius** is a load-bearing doubt. Do not proceed past this step until each is either:

a) **Verified** — point to evidence (file path, test, API doc, code comment)
b) **Mitigated** — implementation handles the failure case explicitly
c) **Accepted** — risk understood and signed off by the human

### Step 4: Implement With Doubt Markers

When writing code, mark unverified assumptions inline:

```js
// DOUBT: concurrent calls assumed impossible — add mutex if usage pattern changes
function processItem(id) { ... }
```

These markers become review hooks: the PR reviewer knows exactly where to focus.

### Step 5: Close Doubts Before Ship

Before marking the task done, resolve all doubt markers:
- Remove the marker and add an evidence comment, OR
- Convert to a tracked issue if the risk is accepted

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
