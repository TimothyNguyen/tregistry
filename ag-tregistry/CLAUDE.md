# CLAUDE.md

This project vendors its Claude/Codex agent toolchain under `tstack/`.

## Read First

- runtime inventory backend: `app/services/runtime_inventory.py`
- vendored Claude artifact: `tstack/.agent/CLAUDE.md`
- vendored install manifest: `tstack/.agent/install-manifest.json`
- vendored MCP settings: `tstack/.agent/settings.json`

## Claude Pickup

Claude should not infer callable agents from `tstack/.agent/skills/` alone.

Use runtime inventory state:

- `/api/runtime/summary`
- `/api/runtime/agents`
- `/api/runtime/skills`
- `/api/runtime/mcps`
- `/api/runtime/hosts`

These endpoints are source of truth for:

- installed agents
- installed skills
- configured MCPs
- host wiring
- bridged vs non-bridged runtime state

## Workflow

When changing this project:

1. patch backend/runtime contract
2. patch frontend inventory view
3. run `pytest`
4. run `npm run build` in `web`

If runtime pickup changes, keep this file and `AGENTS.md` aligned with vendored `tstack/.agent/*` artifacts.
