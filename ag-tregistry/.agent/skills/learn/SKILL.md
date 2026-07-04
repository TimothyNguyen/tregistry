---
name: learn
version: 0.1.1
description: |
  Knowledge capture workflow. Extracts Q&A flashcards from agent session context.
  Writes to local learn-out/ folder as JSON. Exports Quizlet-compatible CSV via
  learn/export.py. Optionally pushes cards to Confluence via atlassian-docs.
  Invoke via /learn at end of any session.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [swe, qa-agent, pm, spec-agent, orchestrate, data, cloud, security, design-agent, migration, release-agent, interviewer]
optional_skills: [atlassian-docs]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Learn

Extract reusable Q&A flashcards from the current session and persist them locally.

## When to invoke

Invoke at the end of any session where new knowledge was produced:
- After implementing a feature (what did we decide and why)
- After debugging (what was the root cause, what does it teach)
- After spec writing (key product decisions)
- After any multi-agent orchestration run

## Workflow

1. **Extract** — from the current session context, generate 3–10 Q&A pairs covering
   decisions, patterns, pitfalls, and product knowledge. Use this prompt pattern:

   > "From this session, extract Q&A flashcards. For each card:
   > - `front`: a clear question someone unfamiliar with this would ask
   > - `back`: a precise, self-contained answer
   > - `deck`: topic or agent name (e.g. 'swe', 'product', 'architecture')
   > - `tags`: 2–4 relevant tags"

2. **Write** — call `learn/export.py --ingest` passing the extracted JSON array via stdin.
   The script appends to `learn-out/cards.json` and writes per-deck files.

3. **Confirm** — print the output: `Captured N cards → deck: <name>`

4. **Confluence (optional)** — if `--push-confluence` was passed, invoke `atlassian-docs`
   to create or update a Confluence page with the new cards table.

## Invocation

```
/learn                           # capture from current session context
/learn --deck product            # override deck name for all cards
/learn --push-confluence         # capture + push to Confluence
```

## Export (separate from capture)

```bash
python learn/export.py --deck swe --format quizlet          # → swe-cards.csv
python learn/export.py --all --format quizlet               # → all-cards.csv
python learn/export.py --since 2026-06-01 --format quizlet  # date-filtered
python learn/export.py --deck swe --confluence --page-title "SWE Learnings"
```

## Card schema

```json
{
  "id": "<uuid4>",
  "front": "question text",
  "back": "answer text",
  "deck": "swe",
  "source_agent": "swe",
  "tags": ["workflow", "debugging"],
  "created_at": "2026-06-25T10:00:00Z"
}
```

## Error handling

| Condition | Behavior |
|-----------|----------|
| `learn-out/` missing | Auto-created |
| `cards.json` malformed | Backed up as `cards.json.bak`, fresh file started |
| Confluence push fails | Local write succeeds, error printed, non-fatal |
| LLM extracts 0 cards | Warning printed, exits 0, no write |
| Duplicate card (same front) | Skipped silently |

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.
