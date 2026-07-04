# ag-tregistry

FastAPI + SQLAlchemy + React agent registry that imports agents, skills, and MCP servers from a local [`agent-architecture`](https://github.com/TimothyNguyen/tstack) install.

## Requirements

- Python 3.11+
- Node.js 18+ (frontend + agent-architecture install scripts)

## Setup

### 1. Clone the vendored runtime

```bash
git clone https://github.com/TimothyNguyen/tstack tstack
```

### 2. Install agent-architecture artifacts

```bash
cd tstack/agent-architecture
node scripts/install.mjs --target ../.agent
cd ../..
```

This writes agents, skills, and host prompts to `tstack/.agent/`.

### 3. Install Python dependencies

```bash
python -m venv .venv

# Windows
.venv\Scripts\python -m pip install -e .[dev]

# macOS / Linux
.venv/bin/pip install -e .[dev]
```

### 4. Start the backend

```bash
# Windows
.venv\Scripts\python -m uvicorn app.main:app --reload

# macOS / Linux
.venv/bin/uvicorn app.main:app --reload
```

API runs at `http://localhost:8000`. Interactive docs at `/docs`.

### 5. Start the frontend (optional)

```bash
cd web
npm install
npm run dev
```

UI runs at `http://localhost:5173`.

## Upgrade agent-architecture

Pull tstack and re-run the install to sync agents, skills, and host artifacts:

```bash
cd tstack && git pull origin master && cd ..
cd tstack/agent-architecture
node scripts/install.mjs --upgrade --target ../.agent
cd ../..
```

Then POST `/api/imports/agent-architecture` to sync the artifact database.

## Environment variables

All variables are prefixed `AG_TREGISTRY_`. Set via `.env` file or shell environment.

| Variable | Default | Description |
|---|---|---|
| `AG_TREGISTRY_DATABASE_URL` | `sqlite:///./ag_tregistry.db` | SQLAlchemy DB URL |
| `AG_TREGISTRY_AGENT_ARCHITECTURE_ROOT` | `tstack/agent-architecture` | Path to agent-architecture source |
| `AG_TREGISTRY_AGENT_INSTALL_ROOT` | `tstack/.agent` | Path to installed agent artifacts |
| `AG_TREGISTRY_ACTIVE_RUNTIME` | *(unset)* | Active host runtime: `claude`, `codex`, or `copilot` |
| `AG_TREGISTRY_RUNTIME_BRIDGED` | *(unset)* | Set `1` when the runtime is wired into the registry |

## API reference

### Catalog (v0)

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/v0/agents` | List installed agents |
| `GET` | `/api/v0/skills` | List installed skills |
| `GET` | `/api/v0/servers` | List configured MCP servers |
| `GET` | `/api/v0/prompts` | List host prompt artifacts |
| `GET` | `/api/v0/deployments` | List deployments (`?namespace=default`) |
| `POST` | `/api/v0/deployments` | Create deployment |
| `DELETE` | `/api/v0/deployments/{name}` | Delete deployment |

### Artifacts

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/artifacts` | List artifacts (`?kind=agent\|skill\|mcp_server`) |
| `POST` | `/api/artifacts` | Upsert artifact |

### Imports

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/imports/agent-architecture` | Sync agents + skills from install manifest |

### Runtime inventory

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/runtime/snapshot` | Full runtime snapshot |
| `GET` | `/api/runtime/summary` | Runtime summary (counts + status) |
| `GET` | `/api/runtime/agents` | Installed agents with callable state |
| `GET` | `/api/runtime/skills` | Installed skills with callable state |
| `GET` | `/api/runtime/mcps` | Configured MCP servers |
| `GET` | `/api/runtime/hosts` | Host bridge status (claude / codex / copilot) |

### Health

```
GET /api/health  →  {"status": "ok"}
```

## CLI

After `pip install -e .[dev]` the `aa` command is available:

```bash
aa list-agents
aa list-skills
aa list-mcps
aa list-prompts
aa list-deployments
aa deploy agent <name> [--namespace <ns>]
aa remove <name> [--namespace <ns>]
```

## Development

### Run tests

```bash
pytest
```

Coverage report is printed automatically (target: ≥95%).

### Lint

```bash
ruff check app tests imports
```

Auto-fix:

```bash
ruff check --fix app tests imports
```

### Type check

```bash
mypy app imports
```

### Check all three

```bash
ruff check app tests imports && mypy app imports && pytest
```
