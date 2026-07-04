---
name: adapter-docker-mcp
version: 0.1.1
description: |
  Docker MCP Registry and Toolkit adapter. Wires 300+ pre-built containerized
  MCP servers (GitHub, Postgres, Playwright, Slack, Stripe, Docker ops, etc.)
  through the Docker MCP Gateway — one stdio multiplexer replaces N individual
  server configs. Use when deploying via Docker or consuming tools from the
  official docker/mcp-registry catalog.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [cloud, release-agent, orchestrate, swe, _infrastructure]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Docker MCP Adapter

Use when connecting agent tools from the Docker MCP Registry, or when the
deployment target is Docker containers.

## What the Docker MCP Gateway Is

`docker mcp gateway run --profile <name>` is a single stdio MUX. It routes
requests to any Docker-packaged MCP server declared in the named profile.
The client configures one entry; the gateway owns container lifecycle,
credential injection, and network isolation.

**Requires Docker Desktop 4.62+** with MCP Toolkit enabled.

## Consumer Config (`.agent-config.json`)

Add one MCP entry pointing to the gateway. Docker Desktop handles profile
resolution and container startup.

```json
{
  "mcps": [
    {
      "name": "docker-gateway",
      "command": "docker",
      "args": ["mcp", "gateway", "run", "--profile", "my-project"]
    }
  ]
}
```

Or use the installer flag to inject it without editing the config file:

```bash
# Default profile "default"
npx agent-architecture install --docker-mcp

# Named profile
npx agent-architecture install --docker-mcp my-project

# Combine flags
npx agent-architecture install --private --docker-mcp backend --hosts claude,codex
```

## Profile Management

Profiles group servers by project or environment. Manage via Docker Desktop
**MCP Toolkit → Profiles** tab or the CLI:

```bash
# Browse and add servers to a profile via Docker Desktop UI
open https://hub.docker.com/mcp

# Pull a private / org-internal catalog (OCI reference)
docker mcp catalog pull <oci-reference>

# List servers in a profile
docker mcp server list --profile my-project
```

## Commonly Used Catalog Servers

| Server | Docker image | Capabilities |
|--------|-------------|--------------|
| Docker ops | `mcp/docker` | `docker build`, `push`, compose lifecycle |
| GitHub | `mcp/github` | PRs, issues, commits, branches |
| Postgres | `mcp/postgres` | SQL queries, schema inspection |
| Playwright | `mcp/playwright` | Browser automation, screenshots |
| Slack | `mcp/slack` | Send messages, read channels |
| Stripe | `mcp/stripe` | Payment intents, customers |
| Filesystem | `mcp/filesystem` | Scoped read/write of declared paths |

Full catalog: `hub.docker.com/mcp`
Registry source: `github.com/docker/mcp-registry`

## Deploying to Docker (cloud agent usage)

When the task is building or shipping Docker images, add `mcp/docker` to the
profile. The gateway exposes Docker build/push/compose tools. Always gate:

- `docker push` → `writes: approval-required`
- `docker system prune` → `careful` skill required
- Registry login → credentials via Docker Secrets, never plain text

## Policy Constraints

- Docker socket required (`/var/run/docker.sock` or Docker Desktop daemon).
- Catalog servers run as isolated containers — no host access beyond declared mounts.
- Egress from inside container servers requires explicit policy approval.
- Profile isolation: treat each profile as a separate trust boundary.
- Declare only servers needed for this project; unused servers expand attack surface.
- `credentialEnvVars` in config for env-based auth; never commit credential values.
- Remote servers (URL-based, not container) bypass container isolation — additional
  egress approval required.

## Doctor Check

```bash
npx agent-architecture doctor
```

If `docker-gateway` appears in the installed `settings.json`, doctor verifies:
- `docker info` exits 0 — Docker daemon is running
- `docker mcp --help` exits 0 — MCP Toolkit available (Docker Desktop 4.62+)

## References

- Catalog: `hub.docker.com/mcp`
- Registry source: `github.com/docker/mcp-registry`
- Docker Desktop MCP Toolkit docs: `docs.docker.com/ai/mcp-catalog-and-toolkit/`

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
