---
name: seniorswe-concise-help
version: 0.1.1
description: |
  Quick-reference card for Senior SWE Concise mode: all levels, skills, and
  commands in one view. One-shot display, not a persistent mode. Invoke via
  /seniorswe-concise-help or "what are the seniorswe-concise commands", "how
  do I use seniorswe-concise", "seniorswe-concise help".
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [swe, _infrastructure]
---

# Senior SWE Concise: Quick Reference

Display this reference card when invoked. One-shot, do NOT change mode,
write flag files, or persist anything.

## Levels

| Level | Trigger | What change |
|-------|---------|-------------|
| **Lite** | `/seniorswe-concise lite` | Build what's asked, name the lazier alternative in one line. |
| **Full** | `/seniorswe-concise` | The ladder enforced: YAGNI -> stdlib -> native -> one line -> minimum. Default. |
| **Ultra** | `/seniorswe-concise ultra` | YAGNI extremist. Deletion before addition. Challenges requirements before building. |

Level sticks until changed or session end.

## Skills

| Skill | Trigger | What it does |
|-------|---------|--------------|
| **seniorswe-concise** | `/seniorswe-concise` | Lazy mode itself. Simplest solution that works. |
| **seniorswe-concise-review** | `/seniorswe-concise-review` | Over-engineering review: `L42: yagni: factory, one product. Inline.` |
| **seniorswe-concise-audit** | `/seniorswe-concise-audit` | Whole-repo bloat audit ranked by cut size. |
| **seniorswe-concise-debt** | `/seniorswe-concise-debt` | Harvest `seniorswe-concise:` comments into a tracked debt ledger. |
| **seniorswe-concise-gain** | `/seniorswe-concise-gain` | Measured-impact scoreboard: less code, less cost, more speed. |
| **seniorswe-concise-help** | `/seniorswe-concise-help` | This card. |

## Deactivate

Say "normal mode" or `/seniorswe-concise off`. Resume anytime with `/seniorswe-concise`.

## Configure Default Mode

Default mode = `full`, auto-active every session. Change it:

**Environment variable** (highest priority):
```bash
export SENIORSWE_CONCISE_DEFAULT_MODE=ultra
```

**Config file** (`~/.config/seniorswe-concise/config.json`):
```json
{ "defaultMode": "lite" }
```

Set `"off"` to disable auto-activation on session start, activate manually
with `/seniorswe-concise` when wanted.

Resolution: env var > config file > `full`.
