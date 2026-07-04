import json
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models import DeploymentRecord
from app.schemas.catalog import (
    DeploymentCondition,
    DeploymentCreate,
    DeploymentDeleteResponse,
    DeploymentEnvelope,
    DeploymentMetadata,
    DeploymentRuntimeRef,
    DeploymentSpec,
    DeploymentStatus,
    DeploymentTargetRef,
)

HOST_PROMPTS = (
    ("claude", "CLAUDE.md"),
    ("codex", "AGENTS.md"),
    ("copilot", "copilot-instructions.md"),
)


def _read_json(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))


def _load_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return _read_json(path)


def _read_description(path: Path, fallback: str) -> str:
    if not path.exists():
        return fallback
    lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines()]
    for line in lines:
        if not line or line.startswith("#") or line.startswith("```") or line.startswith("- "):
            continue
        return line
    return fallback


def _published_meta() -> dict[str, Any]:
    return {
        "io.modelcontextprotocol.registry/official": {
            "publishedAt": datetime.now(tz=UTC).isoformat(),
        }
    }


def _server_meta(command: str) -> dict[str, Any]:
    return {
        "io.modelcontextprotocol.registry/official": {
            "publishedAt": datetime.now(tz=UTC).isoformat(),
        },
        "io.modelcontextprotocol.registry/publisher-provided": {
            "aregistry.ai/metadata": {
                "stars": 0,
                "identity": {
                    "org_is_verified": False,
                    "publisher_identity_verified_by_jwt": False,
                },
                "command": command,
            }
        },
    }


class CatalogService:
    def __init__(self, session: Session | None = None) -> None:
        self.session = session
        self.install_root = settings.agent_install_root
        self.architecture_root = settings.agent_architecture_root
        self.manifest = _load_json_if_exists(self.install_root / "install-manifest.json")
        self.runtime_settings = _load_json_if_exists(self.install_root / "settings.json")
        self.registry = _load_json_if_exists(self.architecture_root / "generated" / "registry.json")

    def list_servers(self) -> list[dict[str, Any]]:
        servers: list[dict[str, Any]] = []
        for name, config in sorted(self.runtime_settings.get("mcpServers", {}).items()):
            command = config.get("command", "")
            args = list(config.get("args", []))
            env = config.get("env", {})
            servers.append(
                {
                    "server": {
                        "name": name,
                        "title": name,
                        "description": f"MCP server configured from vendored repo runtime. Command: {command}",
                        "tag": "latest",
                        "_meta": {
                            "io.modelcontextprotocol.registry/publisher-provided": {
                                "aregistry.ai/metadata": {
                                    "command": command,
                                    "args": args,
                                    "env": sorted(env.keys()),
                                    "installed": self._command_installed(command),
                                }
                            }
                        },
                    },
                    "_meta": _server_meta(command),
                }
            )
        return servers

    def list_skills(self) -> list[dict[str, Any]]:
        skills_root = self.install_root / "skills"
        registry_skills = {item["name"]: item for item in self.registry.get("skills", [])}
        owners_map = self.registry.get("byAgent", {})
        owners_by_skill: dict[str, list[str]] = {}
        for agent_name, skill_names in owners_map.items():
            if agent_name.startswith("_"):
                continue
            for skill_name in skill_names:
                owners_by_skill.setdefault(skill_name, []).append(agent_name)

        skills: list[dict[str, Any]] = []
        for skill_name in self.manifest.get("skills", []):
            skill_path = skills_root / skill_name / "SKILL.md"
            registry_entry = registry_skills.get(skill_name, {})
            skills.append(
                {
                    "skill": {
                        "name": skill_name,
                        "title": skill_name,
                        "description": registry_entry.get(
                            "description",
                            _read_description(skill_path, f"{skill_name} repo skill."),
                        ),
                        "tag": "latest",
                        "source": str(skill_path),
                        "owners": sorted(owners_by_skill.get(skill_name, [])),
                    },
                    "_meta": _published_meta(),
                }
            )
        return skills

    def list_agents(self) -> list[dict[str, Any]]:
        skills_root = self.install_root / "skills"
        agents: list[dict[str, Any]] = []
        for agent_name in self.manifest.get("agents", []):
            skill_path = skills_root / agent_name / "SKILL.md"
            agent_skills = list(self.registry.get("byAgent", {}).get(agent_name, []))
            agents.append(
                {
                    "agent": {
                        "name": agent_name,
                        "description": _read_description(skill_path, f"{agent_name} vendored agent."),
                        "modelProvider": "agent-architecture",
                        "modelName": "host-managed",
                        "tag": "latest",
                        "skills": agent_skills,
                        "source": str(skill_path),
                    },
                    "_meta": _published_meta(),
                }
            )
        return agents

    def list_prompts(self) -> list[dict[str, Any]]:
        prompts: list[dict[str, Any]] = []
        for host_name, filename in HOST_PROMPTS:
            path = self.install_root / filename
            if not path.exists():
                continue
            content = path.read_text(encoding="utf-8")
            prompts.append(
                {
                    "prompt": {
                        "name": host_name,
                        "description": f"{host_name} host prompt artifact.",
                        "content": content,
                        "tag": "latest",
                        "source": str(path),
                    },
                    "_meta": _published_meta(),
                }
            )
        return prompts

    def list_deployments(self, namespace: str = "default") -> list[DeploymentEnvelope]:
        if self.session is None:
            return []
        stmt = select(DeploymentRecord).order_by(DeploymentRecord.created_at.desc())
        if namespace not in {"", "all"}:
            stmt = stmt.where(DeploymentRecord.namespace == namespace)
        records = self.session.scalars(stmt).all()
        return [self._to_deployment(record) for record in records]

    def create_deployment(self, payload: DeploymentCreate) -> DeploymentEnvelope:
        if self.session is None:
            raise RuntimeError("CatalogService requires a database session for deployments.")

        next_name = self._next_deployment_name(payload.resource_name, payload.namespace)
        record = DeploymentRecord(
            id=f"{payload.namespace}/{next_name}",
            resource_type=payload.resource_type,
            resource_name=payload.resource_name,
            tag=payload.tag,
            runtime_id=payload.runtime_id,
            namespace=payload.namespace,
            status="deployed",
            origin="managed",
        )
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        return self._to_deployment(record, name_override=next_name)

    def delete_deployment(self, name: str, namespace: str = "default") -> DeploymentDeleteResponse:
        if self.session is None:
            raise RuntimeError("CatalogService requires a database session for deployments.")
        record_id = f"{namespace}/{name}"
        record = self.session.get(DeploymentRecord, record_id)
        if record is None:
            return DeploymentDeleteResponse(message="Deployment not found.")
        self.session.delete(record)
        self.session.commit()
        return DeploymentDeleteResponse(message=f"Removed deployment {record_id}.")

    def _next_deployment_name(self, resource_name: str, namespace: str) -> str:
        assert self.session is not None
        base = resource_name.lower().replace("_", "-")
        candidate = base
        counter = 2
        while self.session.get(DeploymentRecord, f"{namespace}/{candidate}") is not None:
            candidate = f"{base}-{counter}"
            counter += 1
        return candidate

    def _to_deployment(self, record: DeploymentRecord, name_override: str | None = None) -> DeploymentEnvelope:
        target_kind = "Agent" if record.resource_type == "agent" else "MCPServer"
        timestamp = record.created_at.replace(tzinfo=UTC).isoformat()
        return DeploymentEnvelope(
            metadata=DeploymentMetadata(
                name=name_override or record.id.split("/", 1)[1],
                namespace=record.namespace,
                createdAt=timestamp,
                annotations={"agentregistry.solo.io/origin": record.origin},
            ),
            spec=DeploymentSpec(
                targetRef=DeploymentTargetRef(kind=target_kind, name=record.resource_name, tag=record.tag),
                runtimeRef=DeploymentRuntimeRef(name=record.runtime_id),
                desiredState=record.status,
                env={},
                runtimeConfig={},
            ),
            status=DeploymentStatus(
                conditions=[
                    DeploymentCondition(
                        type="Ready",
                        status="True" if record.status == "deployed" else "False",
                        reason="Deployed" if record.status == "deployed" else "Unknown",
                        message="Managed by ag-tregistry runtime bridge.",
                        lastTransitionTime=timestamp,
                    )
                ]
            ),
        )

    @staticmethod
    def _command_installed(command: str) -> bool:
        if not command:
            return False
        command_path = Path(command)
        if command_path.is_absolute():
            return command_path.exists()
        return shutil.which(command) is not None
