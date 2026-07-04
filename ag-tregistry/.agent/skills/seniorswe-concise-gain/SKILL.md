---
name: seniorswe-concise-gain
version: 0.1.1
description: |
  Show measured impact of concise/lazy-mode coding as a compact scoreboard:
  less code, less cost, more speed, from benchmark medians. One-shot display,
  not a persistent mode. Invoke via /seniorswe-concise-gain, or "what does
  concise mode save", "show impact", "scoreboard".
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [swe]
---

# Senior SWE Concise: Impact Scoreboard

Display this scoreboard when invoked. One-shot: do NOT change mode, write flag
files, or persist anything.

The figures are the published benchmark medians (5 everyday tasks: email
validator, debounce, CSV sum, countdown timer, rate limiter; three models:
Haiku, Sonnet, Opus). They are measured, not computed from the current repo.

## Scoreboard

```
  concise mode gain                 benchmark median / 5 tasks / 3 models

  Lines of code   no-skill    ████████████████████  100%
                  concise     ██▌·················    6-20%   v 80-94%
  Cost            no-skill    ████████████████████  100%
                  concise     █████▌··············   23-53%  v 47-77%
  Speed           concise     > 3-6x faster

  This repo:  /seniorswe-concise-debt  (shortcuts you deferred)
              /seniorswe-concise-audit (what's still cuttable)
```

## Honesty boundary

These are benchmark medians, not this repo. NEVER print a per-repo savings
number ("you saved X lines/tokens here"): the unbuilt version was never
written, so there is no real baseline to subtract from in a live repo. The
only real per-repo figures come from `/seniorswe-concise-debt` (a counted ledger), and
this card points there instead of inventing one.

## Boundaries

One-shot display. Edits nothing, changes no mode.
