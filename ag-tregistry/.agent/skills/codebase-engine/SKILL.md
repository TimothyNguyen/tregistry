---
# Agent skill metadata — name must match the folder name so catalog tests pass.
# allowed-tools restricts which tools this skill may invoke by default;
# shell write, git write, and deploy remain policy-gated (see POLICY_REQUIREMENTS below).
name: codebase-engine
version: 0.1.1
description: |
  Enterprise-safe AST knowledge graph for local codebases. Indexes source
  with tree-sitter, builds a NetworkX graph, clusters by community, and
  answers symbol, path, and dependency queries. No external egress.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [swe, migration, data, orchestrate, qa-agent, spec-agent, cloud, design-agent, interviewer, release-agent, security]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Codebase Engine

<!-- Skill purpose: offline AST indexing + graph query for any local codebase.
     No LLM required for extraction (tree-sitter handles parsing).
     LLM backends are optional and must point to approved internal endpoints. -->

Use this skill to index a local codebase and answer architecture, dependency,
and symbol questions using the `codebase-engine` package.

`codebase-engine` works entirely offline — AST extraction and graph queries
run locally. No data leaves the machine.

## Setup

<!-- One-time install. uv tool install is preferred in enterprise envs because
     it isolates deps and avoids polluting the system Python. -->

Install once per environment:

```bash
pip install codebase-engine
# or
uv tool install codebase-engine
```

Verify:

```bash
codebase-engine --version
```

## Index the Codebase

<!-- extract runs: detect → tree-sitter AST → build NetworkX graph → Leiden cluster.
     Output is codebase-out/graph.json + GRAPH_REPORT.md.
     CODEBASE_OUT lets CI or worktree setups redirect output without touching source. -->

Run from the project root (or pass the path explicitly):

```bash
codebase-engine extract .
# or for a specific directory
codebase-engine extract /path/to/project
```

Output lands in `codebase-out/` by default. Override with `CODEBASE_OUT`:

```bash
CODEBASE_OUT=.codebase-index codebase-engine extract .
```

Index incrementally after changes:

```bash
codebase-engine update
```

Or watch continuously:

```bash
codebase-engine watch
```

## Query

<!-- query uses case-folded substring + IDF against node labels — no stemming,
     no cross-language synonym. If zero results, expand query terms from the
     graph vocabulary (see skills/*/references/query.md for the full protocol). -->

Semantic fuzzy search across the graph:

```bash
codebase-engine query "authentication middleware"
codebase-engine query "database connection pool"
```

Explain a specific symbol:

```bash
codebase-engine explain MyClass
codebase-engine explain handle_request
```

Find the shortest dependency path between two symbols:

```bash
codebase-engine path SymbolA SymbolB
```

Find affected nodes before a change:

```bash
codebase-engine affected src/auth/middleware.py
```

## Workflow

<!-- Step 6 exists because the file watcher debounces at ~500ms; a query
     immediately after an edit may miss the latest nodes. -->

1. Confirm `codebase-engine` is installed (`codebase-engine --version`).
2. Run `codebase-engine extract .` if no index exists (`codebase-out/` absent).
3. Use `codebase-engine query` for broad questions; `codebase-engine explain` for symbols.
4. Use `codebase-engine path` to trace dependency chains.
5. Use `codebase-engine affected` before edits to understand blast radius.
6. Fall back to Grep + Read when the query returns no results (index may lag by ~1s after edits).

## Understanding Workflow

<!-- Use this section when a user asks how a system works, where behavior is
     implemented, what code depends on a module, or what context is needed before a change. -->

Use this workflow when answering architecture, ownership, or dependency questions:

1. Identify the target behavior, symbol, module, or workflow.
2. Check for a knowledge graph index (`codebase-out/` directory with graph files).
   - If present, use `codebase-engine query`, `explain`, `path`, and `affected` for lookups.
   - Spawn an Explore agent for broad questions when using CodeGraph MCP — never call explore tools directly in the main session.
   - Local graph queries only. No external egress.
3. If no index or query returns no results, fall back to local file search (Grep + Read).
4. Summarize entrypoints, data flow, dependencies, and ownership boundaries.
5. Identify tests and docs that verify the behavior.
6. Note uncertainty explicitly.

## Adapter Boundary

<!-- Core workflow functions without any adapter — Grep + Read is always the fallback. -->

Core skill works without any adapter — Grep + Read is always the fallback.
Supported adapters: CodeGraph MCP, any local embedding/index service.
No external APIs, no third-party egress.

## Enterprise Constraints

<!-- These are hard build-time removals, not runtime flags.
     prs.py and wiki.py are absent from this build.
     CODEBASE_ENGINE_LLM_* env vars must point to internal endpoints only. -->

- Local extraction only. No LLM backend required for AST extraction.
- If an LLM backend is configured (`CODEBASE_ENGINE_LLM_*`), it must be an approved internal endpoint.
- No Google Workspace, GitHub PR, or wiki egress in this build.
- Graph files stay in `codebase-out/` (local). Do not upload or sync externally.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
