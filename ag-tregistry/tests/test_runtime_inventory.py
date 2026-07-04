from pathlib import Path

from app.core.config import settings
from app.services.runtime_inventory import build_runtime_snapshot


def test_runtime_snapshot_reads_installed_toolchain():
    snapshot = build_runtime_snapshot()

    assert snapshot.summary.installed_agents >= 10
    assert snapshot.summary.installed_skills >= 10
    assert snapshot.summary.configured_mcps >= 0
    assert "claude" in snapshot.summary.configured_hosts
    assert any(agent.id == "orchestrate" and agent.installed for agent in snapshot.agents)
    assert any(skill.id == "spec" and skill.installed for skill in snapshot.skills)
    assert any(host.id == "codex" and host.installed_artifact for host in snapshot.hosts)


def test_runtime_snapshot_uses_vendored_repo_paths():
    snapshot = build_runtime_snapshot()

    assert Path(snapshot.summary.install_manifest_path) == settings.agent_install_root / "install-manifest.json"
    assert Path(snapshot.summary.settings_path) == settings.agent_install_root / "settings.json"
