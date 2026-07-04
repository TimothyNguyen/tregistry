---
name: pre-commit-review
version: 0.1.0
description: |
  Executable skill that runs pre-commit hooks on code to catch style issues
  (trailing whitespace, debug statements, invalid syntax) before code review.
  Allows reviewers to focus on architecture instead of trivial nitpicks.
  Works across Claude, Codex, and Copilot.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [swe, qa-agent, orchestrate, release-agent, _linter]
metadata:
  support:
    last-reviewed: "2026-06-27"
  platforms: [claude, codex, copilot]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Pre-Commit Code Review

Run pre-commit hooks on code to catch style issues early. Uses pre-commit framework
to detect and fix:

- Trailing whitespace
- Missing final newlines
- Debug statements (pdb, ipdb, breakpoint)
- Invalid JSON/YAML/TOML/XML syntax
- Python syntax errors
- Merge conflict markers
- Large files
- And 40+ other checks

Allows code reviewers to focus on architecture and logic, not formatting nitpicks.

## Quick Start

### Install pre-commit framework
```bash
pip install pre-commit
```

### Configure hooks for your project
Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: debug-statements
      - id: check-ast
```

### Run checks before code review
```bash
pre-commit run --all-files
```

## Platform Usage

### Claude Code (`.claude/skills/pre-commit-review/`)
```bash
/pre-commit-review
# or programmatically:
python ~/.claude/skills/pre-commit-review/run.py --files <file1> <file2>
```

### Codex
Skills load natively. Invoke skill and follow skill instructions.

### Copilot CLI
Use `skill` tool:
```
@pre-commit-review check these files
```

## Core Implementation

**`pre_commit_runner.py`** — Python module that:
- Loads `.pre-commit-config.yaml` from project
- Discovers configured hooks
- Runs pre-commit CLI with proper file filtering
- Parses results into structured format (passed/failed/issues)
- Returns JSON or human-readable output

**Entry points:**
- `run.py` — Claude Code wrapper with formatted output
- CLI: `python pre_commit_runner.py --files <files>`

## Extracted from Pre-Commit Framework

This skill integrates code from the pre-commit repository:

- **Configuration loading** (`clientlib` logic)
- **Hook discovery and filtering** patterns
- **CLI invocation** and result parsing
- **File classification** for hook matching

Pre-commit framework handles:
- Hook environment setup
- Language-specific toolchain management
- Git integration
- Concurrent hook execution

## Typical Workflow

```
1. Develop code locally
   ↓
2. Run: pre-commit run --all-files
   ↓
3. Fix any reported issues
   ↓
4. Commit and push
   ↓
5. Submit for code review
   ↓
6. Reviewer focuses on:
     • Architecture
     • Logic correctness
     • Design patterns
   NOT on:
     • Trailing whitespace
     • Missing newlines
     • Debug statements
```

## Available Checks

### File Quality
- `trailing-whitespace` — trim trailing whitespace
- `end-of-file-fixer` — ensure final newline
- `check-case-conflict` — detect case conflicts
- `check-added-large-files` — prevent large files
- `detect-private-key` — detect hardcoded secrets

### Format Validation
- `check-json` — validate JSON syntax
- `check-yaml` — validate YAML syntax
- `check-toml` — validate TOML syntax
- `check-xml` — validate XML syntax

### Code Quality
- `check-ast` — validate Python syntax
- `debug-statements` — detect pdb/ipdb/breakpoint
- `check-docstring-first` — docstring ordering
- `check-merge-conflict` — detect merge markers

## Integration with Other Skills

**`commit`** — Use pre-commit-review before commit to ensure only
clean code is committed.

**`investigate`** — When debugging tests, pre-commit-review helps
identify debug statements that shouldn't be in production.

**`ship`** — Final check before release: ensure no debug statements,
private keys, or formatting issues.

**`qa`** — QA can run checks to verify code meets style standards
before test execution.

## Configuration Examples

### Minimal (recommended starting point)
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: debug-statements
```

### Python project
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-ast
      - id: debug-statements

  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black

  - repo: https://github.com/PyCQA/isort
    rev: 5.12.0
    hooks:
      - id: isort
```

### Full-featured (enterprise)
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-toml
      - id: check-xml
      - id: check-ast
      - id: debug-statements
      - id: check-docstring-first
      - id: detect-private-key
      - id: check-added-large-files
        args: ['--maxkb=1000']
```

## Troubleshooting

**"No .pre-commit-config.yaml found"**
Create `.pre-commit-config.yaml` in project root with hook definitions.

**"git failed. Is it installed?"**
Pre-commit requires git repository. Run `git init` in project.

**"Hook timed out"**
Some hooks are slow. Increase timeout or run specific hooks only.

**"Hook not found"**
Verify hook `id` matches the `.pre-commit-config.yaml` definition.

## Testing

```bash
npm test              # Full test suite (agent-architecture)
python test_pre_commit_review.py  # Skill-specific tests (8 tests, all passing)
```

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
