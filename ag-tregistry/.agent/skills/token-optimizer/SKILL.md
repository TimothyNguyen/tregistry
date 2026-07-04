---
name: token-optimizer
version: 0.1.1
description: |
  Token reduction for Python objects, API responses, logs, diffs, and code
  before LLM injection. Bundles Python Token Killer (ptk) with zero required
  dependencies and a bundled fallback. Complements rtk-token-optimizer
  (rtk = shell output, token-optimizer = structured data and Python objects).
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [swe, qa-agent, data, orchestrate]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Token Optimizer

Use this skill when compressing structured data, API responses, logs, diffs, or
code before feeding them into an LLM context window.

PTK auto-detects content type and applies the right compression strategy. No
configuration required. Zero external dependencies.

## Detection

PTK auto-detects these types (override with `--type` when needed):

| Type | Triggers on |
|------|------------|
| `dict` | Python dicts, JSON objects |
| `list` | Python lists, JSON arrays |
| `code` | Files with `def`, `class`, `import`, `function`, etc. |
| `log` | Lines with `[ERROR]`, `PASSED`, `FAILED`, `INFO:`, etc. |
| `diff` | Unified diff with `@@` hunks |
| `text` | Everything else |

## Setup

Prefer the installed package when available:

```bash
pip install python-token-killer
# or
uv add python-token-killer
```

If unavailable, use the bundled CLI (no install needed — Python 3.10+ only):

```bash
# installed to {target}/token-optimizer/ — default install target is .agent/
python .agent/token-optimizer/ptk_minimize.py <file>
```

## Usage

### Compress a file

```bash
python .agent/token-optimizer/ptk_minimize.py data/large_response.json
python .agent/token-optimizer/ptk_minimize.py --stats data/response.json
```

### Pipe stdin

```bash
cat server.log | python .agent/token-optimizer/ptk_minimize.py --stdin --type log
cat diff.patch | python .agent/token-optimizer/ptk_minimize.py --stdin --type diff
curl -s https://api.example.com/data | python .agent/token-optimizer/ptk_minimize.py --stdin
```

### Aggressive mode (max compression)

```bash
python .agent/token-optimizer/ptk_minimize.py --aggressive --stats large_file.json
cat build.log | python .agent/token-optimizer/ptk_minimize.py --stdin --type log --aggressive
```

### From Python (in agent scripts or tool wrappers)

```python
import sys
sys.path.insert(0, ".agent/token-optimizer/lib")
import ptk

# Any Python object
minimized = ptk.minimize(api_response)
stats = ptk.stats(api_response)  # includes savings_pct
print(f"Saved {stats['savings_pct']}% tokens")
```

## When to Apply

Use ptk before injecting any of these into LLM context:

- API responses with null fields, empty arrays, empty dicts
- Log output from pytest, cargo test, go test, Docker, CI
- Git diffs with large unchanged context blocks
- Code files when only signatures matter (use `--aggressive`)
- Large JSON datasets (list-of-dicts → tabular, saves 50–80%)
- Natural language with filler phrases (use `--type text`)

## Rules

- Do not run ptk on security-sensitive data (credentials, tokens, PII) — strip
  those before minimizing.
- Do not use aggressive mode when full stack traces are needed for debugging.
- Do not minimize raw JSON contracts used in snapshot or contract tests.
- Fall back to raw output when compressed output lacks enough context.
- Record compression stats in the response when savings exceed 30%.

## Complement: RTK

Use rtk for shell command output; use ptk for Python objects and structured data:

```bash
rtk git status          # shell output → rtk
rtk pytest              # noisy test runner stdout → rtk
ptk.minimize(response)  # API JSON dict → ptk
ptk.minimize(log_text)  # structured log string → ptk
```

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
