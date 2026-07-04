---
name: rtk-token-optimizer
version: 0.1.1
description: |
  Optional Rust Token Killer integration guidance. Uses RTK to reduce noisy shell output
  when installed and approved by policy. Does not install global hooks or enable telemetry by default.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [_infrastructure, swe, data]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# RTK Token Optimizer

Use this workflow when the user asks to reduce token cost, compress command
output, or use Rust Token Killer.

RTK is optional. Do not assume it is installed.

## Rules

- Do not run `curl | sh`.
- Do not install global hooks without explicit user and policy approval.
- Do not enable RTK telemetry.
- Prefer repo-local documentation and explicit command usage first.
- Use raw command output when debugging requires full details.
- Tell the user when RTK may hide relevant output.

## Steps

1. Check whether `rtk` is on PATH with `rtk --version`.
2. If absent, point to `docs/rtk-token-optimizer.md` for approved install options.
3. If present, prefer explicit wrappers for noisy commands:
   - `rtk git status`
   - `rtk git diff`
   - `rtk grep "pattern" .`
   - `rtk find "*.md" .`
   - `rtk test <command>`
   - `rtk playwright test`
   - `rtk pytest`
4. For failures, rerun the underlying raw command when compressed output is
   insufficient.
5. Record whether RTK was used in the response.

## Recommended Usage

Use RTK for broad, noisy inspection:

```bash
rtk git status
rtk git diff
rtk grep "TODO" .
rtk find "*.md" .
```

Avoid RTK for exact output needs:

- Snapshot tests.
- Full stack traces.
- Raw JSON contracts.
- Security-sensitive logs.
- Commands where every line matters.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
