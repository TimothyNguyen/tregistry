# AGENTS.md

This project vendors its agent toolchain under `tstack/`.

## Read First

- runtime inventory backend: `app/services/runtime_inventory.py`
- vendored install manifest: `tstack/.agent/install-manifest.json`
- vendored MCP settings: `tstack/.agent/settings.json`
- vendored skill install: `tstack/.agent/skills/`
- vendored registry source: `tstack/agent-architecture/generated/registry.json`

## Runtime Truth

Do not assume installed-on-disk means callable in current session.

Use `/api/runtime/snapshot` or the web UI to distinguish:

- installed
- configured
- callable in repo runtime
- callable in current runtime

## Vendored Agents

Current vendored install includes:

- `swe`
- `qa-agent`
- `spec-agent`
- `pm`
- `orchestrate`
- `cloud`
- `data`
- `design-agent`
- `diagram-agent`
- `interviewer`
- `migration`
- `migration-engineer`
- `release-agent`
- `security`

## Codex Notes

- Codex should treat `tstack/.agent/AGENTS.md` as installed host artifact reference.
- Prefer runtime inventory routes over guessing from filesystem fragments.
- When changing install/runtime behavior, update tests and verify `web` build plus `pytest`.
