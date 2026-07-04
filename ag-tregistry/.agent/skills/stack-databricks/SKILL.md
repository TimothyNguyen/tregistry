---
name: stack-databricks
version: 0.1.1
description: |
  Databricks engineering workflows for Asset Bundles, jobs, notebooks, SDK
  usage, and governed data access.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [data]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Databricks

Use for Databricks jobs, notebooks, Asset Bundles, workspace automation, and
data-platform code.

## References

- `databricks/databricks-agent-skills`: skill-pack pattern reference. **Vendored** under `databricks-agent-skills/`.
- `databricks/databricks-sdk-py`: optional SDK adapter pattern. **Reference subset vendored** under `databricks-sdk-py/` (examples + curated docs; install runtime via `pip install databricks-sdk`).
- `databricks/bundle-examples`: Asset Bundle examples. **Vendored** under `bundle-examples/`.

## Vendored Skill Packs (stable)

Activate the matching pack only when the user is working in that product area.
Each pack folder holds a `SKILL.md` with its own activation rules.

| Pack | Use it for |
|---|---|
| `databricks-agent-skills/skills/databricks-core` | Parent skill: CLI auth, profiles, data exploration, Genie. Load first for any Databricks task. |
| `databricks-agent-skills/skills/databricks-dabs` | Databricks Asset Bundles authoring, validation, deploy dry-runs. |
| `databricks-agent-skills/skills/databricks-jobs` | Lakeflow Jobs development and scheduling. |
| `databricks-agent-skills/skills/databricks-pipelines` | Lakeflow Spark Declarative Pipelines (batch + streaming). |
| `databricks-agent-skills/skills/databricks-apps` | Full-stack TypeScript Databricks Apps. |
| `databricks-agent-skills/skills/databricks-app-design` | UX/design guidance for Databricks Apps. |
| `databricks-agent-skills/skills/databricks-lakebase` | Lakebase Postgres autoscaling project management. |
| `databricks-agent-skills/skills/databricks-model-serving` | Model Serving endpoints and inference. |
| `databricks-agent-skills/skills/databricks-vector-search` | Vector Search index design and queries. |
| `databricks-agent-skills/skills/databricks-serverless-migration` | Classic-to-serverless compute migrations. |

## Vendored Skill Packs (experimental — opt-in only)

Skills under `databricks-agent-skills/experimental/` are not policy-stable.
Use only when the active profile permits experimental tooling. Examples:
`databricks-unity-catalog`, `databricks-mlflow-evaluation`,
`databricks-spark-structured-streaming`, `databricks-genie`,
`databricks-aibi-dashboards`, `databricks-iceberg`,
`databricks-lakeflow-connect`, `databricks-python-sdk`. See
`databricks-agent-skills/experimental/README.md` for the full list.

## Asset Bundle Examples

`bundle-examples/` mirrors the upstream `databricks/bundle-examples` repo:
`default_python`, `default_sql`, `default_minimal`, `dbt_sql`,
`lakeflow_pipelines_python`, `lakeflow_pipelines_sql`, `mlops_stacks`,
`pydabs`, `knowledge_base`, `contrib/`. Use as templates only — replace
workspace hosts, profiles, and secret scopes with project-local values
before deploying.

## SDK Reference

`databricks-sdk-py/` carries only documentation + examples (Apache-2.0). The
runtime library is **not** vendored; install with `pip install databricks-sdk`
when the active policy allows. See `databricks-sdk-py/docs/authentication.md`
for the supported auth modes (env vars, `.databrickscfg`, OAuth,
service-principal) — never embed PATs or workspace URLs with embedded creds
in code or commits.

## Skill Activation Rules

- Match user intent to one pack first; load `databricks-core` plus the
  matching product pack. Do not inline every skill.
- Experimental packs must be explicitly named by the user or enabled by
  policy before activating.
- Bundle examples are templates; do not deploy them as-is.
- All vendored skills inherit the Enterprise Preamble above. Skip or gate any
  vendored guidance that calls public telemetry, public update checks, or
  unscoped credential reads.

## Workflow

- Inventory bundles, jobs, notebooks, cluster policies, secrets usage, and data permissions.
- Keep workspace mutations approval-gated.
- Prefer local validation and bundle dry-runs before deploys.
- Avoid embedding tokens, workspace URLs with secrets, or raw data extracts in outputs.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
