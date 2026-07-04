import json
import os
import shutil
from pathlib import Path
from typing import Any, cast

from app.core.config import settings
from app.schemas.runtime import (
    RuntimeAgentRead,
    RuntimeHostRead,
    RuntimeMcpRead,
    RuntimeSkillRead,
    RuntimeSnapshot,
    RuntimeSummary,
)

SUPPORTED_CALLABLE_HOSTS = ("claude", "codex", "copilot")
HOST_ARTIFACT_FILES = {
    "claude": "CLAUDE.md",
    "codex": "AGENTS.md",
    "copilot": "copilot-instructions.md",
}


def _read_json(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))


def _load_optional_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return _read_json(path)


def _load_registry_maps(agent_architecture_root: Path) -> tuple[dict, dict]:
    generated_root = agent_architecture_root / "generated"
    registry = _load_optional_json(generated_root / "registry.json")
    skills_index = _load_optional_json(generated_root / "skills.index.json")
    registry_skills = {
        skill["name"]: skill for skill in registry.get("skills", [])
    }
    indexed_skills = {
        skill["name"]: skill for skill in skills_index.get("skills", [])
    }
    for name, skill in indexed_skills.items():
        registry_skills.setdefault(name, skill)
    return registry, registry_skills


def _invert_registry_owners(registry: dict) -> dict[str, list[str]]:
    owners: dict[str, list[str]] = {}
    for agent_name, skill_names in registry.get("byAgent", {}).items():
        if agent_name.startswith("_"):
            continue
        for skill_name in skill_names:
            owners.setdefault(skill_name, []).append(agent_name)
    return owners


def _installed_skill_names(agent_install_root: Path) -> set[str]:
    skills_root = agent_install_root / "skills"
    if not skills_root.exists():
        return set()
    return {entry.name for entry in skills_root.iterdir() if entry.is_dir()}


def _normalize_runtime() -> tuple[str, bool]:
    runtime = os.getenv("AG_TREGISTRY_ACTIVE_RUNTIME", "none").strip().lower() or "none"
    bridged = os.getenv("AG_TREGISTRY_RUNTIME_BRIDGED", "").strip().lower() in {"1", "true", "yes", "on"}
    if runtime not in {*SUPPORTED_CALLABLE_HOSTS, "none"}:
        return "none", False
    return runtime, bridged


def _host_artifact_status(
    agent_install_root: Path, configured_hosts: list[str]
) -> tuple[dict[str, bool], list[RuntimeHostRead]]:
    current_runtime, runtime_bridged = _normalize_runtime()
    artifact_status: dict[str, bool] = {}
    hosts: list[RuntimeHostRead] = []

    for host in SUPPORTED_CALLABLE_HOSTS:
        artifact_path = agent_install_root / HOST_ARTIFACT_FILES[host]
        installed_artifact = artifact_path.exists()
        artifact_status[host] = installed_artifact
        configured = host in configured_hosts
        supported_by_current_runtime = host == current_runtime
        callable_now = configured and installed_artifact and runtime_bridged and supported_by_current_runtime
        hosts.append(
            RuntimeHostRead(
                id=host,
                configured=configured,
                artifact_path=str(artifact_path),
                installed_artifact=installed_artifact,
                supported_by_current_runtime=supported_by_current_runtime,
                callable_now=callable_now,
            )
        )

    return artifact_status, hosts


def _callable_hosts(configured_hosts: list[str], artifact_status: dict[str, bool]) -> list[str]:
    return [
        host for host in configured_hosts
        if host in SUPPORTED_CALLABLE_HOSTS and artifact_status.get(host, False)
    ]


def _command_installed(command: str) -> bool:
    command_path = Path(command)
    if command_path.is_absolute():
        return command_path.exists()
    return shutil.which(command) is not None


def _status_message(configured_hosts: list[str], current_runtime: str, runtime_bridged: bool) -> str:
    if not configured_hosts:
        return "No repo runtime hosts configured."
    if current_runtime == "none":
        return "Repo runtime configured. Current session runtime not declared."
    if not runtime_bridged:
        hosts_str = ", ".join(configured_hosts)
        return f"Repo runtime configured for {hosts_str}. Current {current_runtime} runtime not bridged."
    return f"{current_runtime} runtime bridged. Installed repo runtime is callable now."


def build_runtime_snapshot(
    agent_architecture_root: Path | None = None,
    agent_install_root: Path | None = None,
) -> RuntimeSnapshot:
    architecture_root = agent_architecture_root or settings.agent_architecture_root
    install_root = agent_install_root or settings.agent_install_root

    manifest_path = install_root / "install-manifest.json"
    settings_path = install_root / "settings.json"
    manifest = _load_optional_json(manifest_path)
    runtime_settings = _load_optional_json(settings_path)
    registry, registry_skills = _load_registry_maps(architecture_root)
    skill_owners = _invert_registry_owners(registry)
    installed_skill_names = _installed_skill_names(install_root)
    configured_hosts = manifest.get("hosts", [])
    current_runtime, runtime_bridged = _normalize_runtime()
    artifact_status, hosts = _host_artifact_status(install_root, configured_hosts)
    callable_hosts = _callable_hosts(configured_hosts, artifact_status)

    agents: list[RuntimeAgentRead] = []
    for agent_name in manifest.get("agents", []):
        indexed_skill = registry_skills.get(agent_name, {})
        agent_call_hosts = list(callable_hosts)
        agents.append(
            RuntimeAgentRead(
                id=agent_name,
                description=indexed_skill.get("description", f"{agent_name} agent."),
                source_path=str(architecture_root / indexed_skill.get("path", f"agents/{agent_name}/SKILL.md.tmpl")),
                installed=agent_name in installed_skill_names,
                enabled=True,
                indexed=agent_name in registry_skills,
                callable_hosts=agent_call_hosts,
                active_runtime=current_runtime,
                callable_now=runtime_bridged and current_runtime in agent_call_hosts,
            )
        )

    skills: list[RuntimeSkillRead] = []
    for skill_name in manifest.get("skills", []):
        indexed_skill = registry_skills.get(skill_name, {})
        skill_call_hosts = list(callable_hosts)
        skills.append(
            RuntimeSkillRead(
                id=skill_name,
                description=indexed_skill.get("description", ""),
                source_path=str(architecture_root / indexed_skill.get("path", f"{skill_name}/SKILL.md.tmpl")),
                owners=sorted(skill_owners.get(skill_name, indexed_skill.get("agents", []))),
                installed=skill_name in installed_skill_names,
                indexed=skill_name in registry_skills,
                callable_hosts=skill_call_hosts,
                active_runtime=current_runtime,
                callable_now=runtime_bridged and current_runtime in skill_call_hosts,
            )
        )

    mcps: list[RuntimeMcpRead] = []
    for mcp_name, mcp_config in runtime_settings.get("mcpServers", {}).items():
        env_map = mcp_config.get("env", {})
        mcps.append(
            RuntimeMcpRead(
                id=mcp_name,
                command=mcp_config.get("command", ""),
                args=list(mcp_config.get("args", [])),
                env_refs=sorted(env_map.keys()),
                configured=True,
                installed=_command_installed(mcp_config.get("command", "")),
                running=False,
                connected_to_current_runtime=runtime_bridged and current_runtime in callable_hosts,
                callable_hosts=list(callable_hosts),
            )
        )

    agents.sort(key=lambda item: item.id)
    skills.sort(key=lambda item: item.id)
    mcps.sort(key=lambda item: item.id)
    hosts.sort(key=lambda item: item.id)

    summary = RuntimeSummary(
        current_runtime=current_runtime,
        runtime_bridged=runtime_bridged,
        status_message=_status_message(configured_hosts, current_runtime, runtime_bridged),
        configured_hosts=configured_hosts,
        installed_agents=len(agents),
        installed_skills=len(skills),
        configured_mcps=len(mcps),
        install_manifest_path=str(manifest_path),
        settings_path=str(settings_path),
    )

    return RuntimeSnapshot(
        summary=summary,
        agents=agents,
        skills=skills,
        mcps=mcps,
        hosts=hosts,
    )
