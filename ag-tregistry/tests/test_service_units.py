"""
Unit tests for catalog.py and runtime_inventory.py helper functions and
edge-case branches that route-level tests cannot easily exercise.
"""
import json

import pytest

from app.services.catalog import (
    CatalogService,
    _load_json_if_exists,
    _read_description,
)
from app.services.runtime_inventory import (
    _installed_skill_names,
    _normalize_runtime,
    _status_message,
    build_runtime_snapshot,
)

# ---------------------------------------------------------------------------
# catalog helpers
# ---------------------------------------------------------------------------

def test_load_json_if_exists_missing_file(tmp_path):
    assert _load_json_if_exists(tmp_path / "nonexistent.json") == {}


def test_load_json_if_exists_present_file(tmp_path):
    p = tmp_path / "data.json"
    p.write_text(json.dumps({"key": "value"}), encoding="utf-8")
    assert _load_json_if_exists(p) == {"key": "value"}


def test_read_description_missing_file(tmp_path):
    result = _read_description(tmp_path / "SKILL.md", fallback="fallback text")
    assert result == "fallback text"


def test_read_description_all_headers_returns_fallback(tmp_path):
    p = tmp_path / "SKILL.md"
    p.write_text("# Title\n\n## Section\n\n```code block```\n- list item\n", encoding="utf-8")
    result = _read_description(p, fallback="my fallback")
    assert result == "my fallback"


def test_read_description_returns_first_prose_line(tmp_path):
    p = tmp_path / "SKILL.md"
    p.write_text("# Title\n\nThis is the description.\n\nMore text.\n", encoding="utf-8")
    result = _read_description(p, fallback="unused")
    assert result == "This is the description."


def test_catalog_list_prompts_skips_missing_host_file(tmp_path):
    # Only claude artifact exists; codex and copilot files absent.
    (tmp_path / "CLAUDE.md").write_text("claude prompt", encoding="utf-8")
    service = CatalogService.__new__(CatalogService)
    service.session = None
    service.install_root = tmp_path
    service.architecture_root = tmp_path
    service.manifest = {}
    service.runtime_settings = {}
    service.registry = {}

    prompts = service.list_prompts()
    assert len(prompts) == 1
    assert prompts[0]["prompt"]["name"] == "claude"


def test_catalog_command_installed_nonabsolute():
    service = CatalogService.__new__(CatalogService)
    assert service._command_installed("") is False
    assert service._command_installed("python") is True
    assert service._command_installed("definitely-not-a-real-binary-xyz") is False


def test_catalog_command_installed_absolute(tmp_path):
    service = CatalogService.__new__(CatalogService)
    real = tmp_path / "mytool"
    real.write_text("x")
    assert service._command_installed(str(real)) is True
    assert service._command_installed(str(tmp_path / "missing")) is False


def test_catalog_list_deployments_no_session():
    service = CatalogService.__new__(CatalogService)
    service.session = None
    assert service.list_deployments() == []


def test_catalog_create_deployment_no_session():
    from app.schemas.catalog import DeploymentCreate
    service = CatalogService.__new__(CatalogService)
    service.session = None
    with pytest.raises(RuntimeError, match="database session"):
        service.create_deployment(DeploymentCreate(
            resourceType="agent", resourceName="swe",
            tag="latest", runtimeId="local", namespace="default",
        ))


def test_catalog_delete_deployment_no_session():
    service = CatalogService.__new__(CatalogService)
    service.session = None
    with pytest.raises(RuntimeError, match="database session"):
        service.delete_deployment("swe")


def test_catalog_delete_deployment_not_found():
    from app.db.session import SessionLocal, init_db
    init_db()
    with SessionLocal() as session:
        service = CatalogService(session)
        result = service.delete_deployment("nonexistent-xyz-99999")
    assert "not found" in result.message.lower()


def test_catalog_deployment_name_collision():
    from app.db.session import SessionLocal, init_db
    from app.schemas.catalog import DeploymentCreate
    init_db()
    with SessionLocal() as session:
        service = CatalogService(session)
        first = service.create_deployment(DeploymentCreate(
            resourceType="agent", resourceName="collision-test",
            tag="latest", runtimeId="local", namespace="col-ns",
        ))
        second = service.create_deployment(DeploymentCreate(
            resourceType="agent", resourceName="collision-test",
            tag="latest", runtimeId="local", namespace="col-ns",
        ))
        assert first.metadata.name != second.metadata.name
        assert second.metadata.name == "collision-test-2"
        service.delete_deployment(first.metadata.name, namespace="col-ns")
        service.delete_deployment(second.metadata.name, namespace="col-ns")


def test_catalog_list_deployments_namespace_filter():
    from app.db.session import SessionLocal, init_db
    from app.schemas.catalog import DeploymentCreate
    init_db()
    with SessionLocal() as session:
        service = CatalogService(session)
        service.create_deployment(DeploymentCreate(
            resourceType="agent", resourceName="ns-filter-test",
            tag="latest", runtimeId="local", namespace="ns-a",
        ))
        ns_a = service.list_deployments(namespace="ns-a")
        ns_b = service.list_deployments(namespace="ns-b")
        assert any(d.spec.target_ref.name == "ns-filter-test" for d in ns_a)
        assert not any(d.spec.target_ref.name == "ns-filter-test" for d in ns_b)
        for d in ns_a:
            if d.spec.target_ref.name == "ns-filter-test":
                service.delete_deployment(d.metadata.name, namespace="ns-a")


# ---------------------------------------------------------------------------
# runtime_inventory helpers
# ---------------------------------------------------------------------------

def test_installed_skill_names_missing_skills_dir(tmp_path):
    result = _installed_skill_names(tmp_path)
    assert result == set()


def test_installed_skill_names_with_dirs(tmp_path):
    (tmp_path / "skills").mkdir()
    (tmp_path / "skills" / "spec").mkdir()
    (tmp_path / "skills" / "review").mkdir()
    (tmp_path / "skills" / "not-a-dir.txt").write_text("x")
    result = _installed_skill_names(tmp_path)
    assert result == {"spec", "review"}


def test_normalize_runtime_invalid_value(monkeypatch):
    monkeypatch.setenv("AG_TREGISTRY_ACTIVE_RUNTIME", "invalid-host")
    monkeypatch.setenv("AG_TREGISTRY_RUNTIME_BRIDGED", "1")
    runtime, bridged = _normalize_runtime()
    assert runtime == "none"
    assert bridged is False


def test_normalize_runtime_valid_bridged(monkeypatch):
    monkeypatch.setenv("AG_TREGISTRY_ACTIVE_RUNTIME", "claude")
    monkeypatch.setenv("AG_TREGISTRY_RUNTIME_BRIDGED", "true")
    runtime, bridged = _normalize_runtime()
    assert runtime == "claude"
    assert bridged is True


def test_status_message_no_configured_hosts():
    msg = _status_message([], "none", False)
    assert "No repo runtime" in msg


def test_status_message_runtime_not_declared():
    msg = _status_message(["claude"], "none", False)
    assert "not declared" in msg


def test_status_message_not_bridged():
    msg = _status_message(["claude"], "claude", False)
    assert "not bridged" in msg


def test_status_message_bridged():
    msg = _status_message(["claude"], "claude", True)
    assert "callable now" in msg


def test_build_snapshot_handles_missing_optional_files(tmp_path):
    arch_root = tmp_path / "arch"
    install_root = tmp_path / "install"
    (arch_root / "generated").mkdir(parents=True)
    (arch_root / "generated" / "registry.json").write_text(
        json.dumps({"skills": [], "byAgent": {}}), encoding="utf-8"
    )
    (install_root).mkdir()

    snapshot = build_runtime_snapshot(
        agent_architecture_root=arch_root,
        agent_install_root=install_root,
    )
    assert snapshot.agents == []
    assert snapshot.skills == []
    assert snapshot.mcps == []
    assert snapshot.summary.installed_agents == 0
