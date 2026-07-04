---
name: seniorswe-concise-debt
version: 0.1.1
description: |
  Harvest every `seniorswe-concise:` comment in the codebase into a debt ledger
  so deliberate shortcuts get tracked instead of rotting into "later means never".
  Invoke via /seniorswe-concise-debt, or "what shortcuts did we defer", "list
  the seniorswe-concise markers", "debt ledger", or "what did we mark to do
  later". One-shot report, changes nothing.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [swe]
---

Every deliberate shortcut made in concise mode is marked with a `seniorswe-concise:`
comment naming its ceiling and upgrade path. This collects them into one ledger
so a deferral can't quietly become permanent.

## Scan

Grep the repo for comment markers, skipping `node_modules`, `.git`, and build
output:

`grep -rnE '(#|//) ?seniorswe-concise:' .`  (add other comment prefixes if your stack uses them)

Each hit is one ledger row. The comment prefix keeps prose that merely mentions
the convention out of the ledger.

## Output

One row per marker, grouped by file:

`<file>:<line>, <what was simplified>. ceiling: <the limit named>. upgrade: <the trigger to revisit>.`

The convention is `seniorswe-concise: <ceiling>, <upgrade path>`, so pull the ceiling
and the trigger straight from the comment. Want an owner per row too? add
`git blame -L<line>,<line>`.

Flag the rot risk: any `seniorswe-concise:` comment that names no upgrade path or
trigger gets a `no-trigger` tag, those are the ones that silently rot.

End with `<N> markers, <M> with no trigger.` Nothing found: `No sc: debt. Clean ledger.`

## Boundaries

Reads and reports only, changes nothing. To persist it, ask and it writes the
ledger to a file (e.g. `SC-DEBT.md`). One-shot. "normal mode" to revert.
