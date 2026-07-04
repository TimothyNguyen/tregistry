---
name: stack-csharp
version: 0.1.1
description: |
  C# and .NET modernization guidance for projects, packages, services, tests,
  analyzers, and compatibility assessments.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [swe, migration]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# C# / .NET Stack

Use for C# projects, .NET services, libraries, test suites, and framework
upgrades.

## Workflow

- Inventory target frameworks, project references, NuGet packages, analyzers,
  build configuration, and service host assumptions.
- Separate mechanical project upgrades from behavior changes.
- Use compatibility reports before rewriting code.
- Prefer targeted tests around changed behavior and startup/config paths.
- Gate database reads, cloud calls, credential reads, and deploys by policy.

## Routes

- Legacy .NET + SQL Server modernization:
  `migration-dotnet-sqlserver-modernization`.
- SQL Server-specific work: `stack-sql-server`.

## Vendored .NET Skill Packs

Upstream: <https://github.com/dotnet/skills> (vendored under `dotnet-skills/`).
Read `dotnet-skills/UPSTREAM_README.md` for the canonical install paths
(Copilot CLI, Claude Code, VS Code, Cursor, Codex). When the host agent
already has the marketplace installed, prefer the marketplace plugin over
the vendored copy.

Plugin → activate when the user is working in that area. Each plugin folder
holds `plugin.json` + a `skills/` directory; each skill folder holds a
`SKILL.md` with its own activation rules.

| Plugin | Use it for |
|---|---|
| `dotnet-skills/plugins/dotnet` | Everyday C# tasks: file-based scripts, P/Invoke, NuGet trusted publishing. |
| `dotnet-skills/plugins/dotnet-aspnetcore` | ASP.NET Core: minimal APIs, file upload, OpenTelemetry wiring, Blazor Server → Web App migration. |
| `dotnet-skills/plugins/dotnet-blazor` | Blazor authoring: components, forms, JS interop, prerendering, auth, project creation. |
| `dotnet-skills/plugins/dotnet-data` | EF Core query optimization (N+1, tracking modes, compiled queries). |
| `dotnet-skills/plugins/dotnet-diag` | Crash dumps, trace collection, dotnet-trace, Android/Apple symbolication, CLR activation debugging, microbenchmarks. |
| `dotnet-skills/plugins/dotnet-msbuild` | MSBuild diagnostics + perf: binlogs, modernization to SDK-style, item/property/target authoring, antipatterns, server mode. |
| `dotnet-skills/plugins/dotnet-nuget` | NuGet workflows: convert project to Central Package Management. |
| `dotnet-skills/plugins/dotnet-upgrade` | Cross-version migrations (.NET 8↔11), nullable references, AOT compatibility, thread abort removal. |
| `dotnet-skills/plugins/dotnet-test` | Test execution, frameworks (MSTest/xUnit/NUnit/TUnit), filter syntax, coverage, gap analysis, test smell detection, xUnit↔MSTest migrations, MTP hot reload. |
| `dotnet-skills/plugins/dotnet-ai` | AI/ML in .NET: MEAI, Semantic Kernel, ML.NET; MCP server skills (create/debug/test/publish). |
| `dotnet-skills/plugins/dotnet-maui` | MAUI: doctor, lifecycle, CollectionView, DI, data binding, safe area, Shell navigation, theming. |
| `dotnet-skills/plugins/dotnet-template-engine` | `dotnet new` templates: discovery, authoring, validation, smart defaults, comparison. |
| `dotnet-skills/plugins/dotnet11` | .NET 11 new APIs (System.Text.Json). |
| `dotnet-skills/plugins/dotnet-experimental` | Experimental: mock usage analysis, SIMD vectorization, test maintainability detection. |

## Skill Activation Rules

- Match user intent to one plugin first, then read that plugin's `plugin.json`
  and the target skill's `SKILL.md` before acting. Do not inline every skill —
  load only what is relevant.
- Skills under `dotnet-msbuild/` activate only inside MSBuild/.NET build
  context. Do not invoke them on non-build tasks.
- Skills under `dotnet-experimental/` are not policy-stable. Use only when the
  active profile permits experimental tooling.
- All vendored skills inherit the Enterprise Preamble above. Vendored guidance
  that calls public telemetry, public update checks, or unscoped credential
  reads must be skipped or gated by policy.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
