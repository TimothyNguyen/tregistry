import json
from pathlib import Path
from typing import Any, cast

from app.schemas.artifacts import ArtifactCreate, ImportSummary


def _load_json(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))


def import_registry(
    registry_path: Path,
    manifest_path: Path | None = None,
) -> tuple[list[ArtifactCreate], ImportSummary]:
    data = _load_json(registry_path)
    manifest: dict = {}
    if manifest_path is not None and manifest_path.exists():
        manifest = _load_json(manifest_path)

    version = manifest.get("version", "latest")
    registry_skills = {s["name"]: s for s in data.get("skills", [])}
    artifacts: list[ArtifactCreate] = []

    # Use manifest as primary source so all installed skills are captured;
    # registry.json is only a subset (generated index, misses adapters/stacks/etc).
    skill_names = manifest.get("skills") or [s["name"] for s in data.get("skills", [])]
    for skill_name in skill_names:
        entry = registry_skills.get(skill_name, {})
        artifacts.append(
            ArtifactCreate(
                id=f"skill:{skill_name}",
                kind="skill",
                name=skill_name,
                version=version,
                description=entry.get("description", ""),
                source=str(registry_path),
            )
        )

    agent_names = manifest.get("agents") or [
        k for k in data.get("byAgent", {}).keys() if not k.startswith("_")
    ]
    for agent_name in agent_names:
        artifacts.append(
            ArtifactCreate(
                id=f"agent:{agent_name}",
                kind="agent",
                name=agent_name,
                version=version,
                description=f"Imported from agent-architecture registry entry {agent_name}.",
                source=str(registry_path),
            )
        )

    mcp_source = str(manifest_path) if manifest_path is not None else str(registry_path)
    for mcp_name in manifest.get("mcps", []):
        artifacts.append(
            ArtifactCreate(
                id=f"mcp:{mcp_name}",
                kind="mcp_server",
                name=mcp_name,
                version=version,
                description="MCP server from agent-architecture install manifest.",
                source=mcp_source,
            )
        )

    summary = ImportSummary(
        imported=len(artifacts),
        agents=sum(1 for a in artifacts if a.kind == "agent"),
        skills=sum(1 for a in artifacts if a.kind == "skill"),
        mcps=sum(1 for a in artifacts if a.kind == "mcp_server"),
        version=version,
        source_registry=str(registry_path),
    )
    return artifacts, summary
