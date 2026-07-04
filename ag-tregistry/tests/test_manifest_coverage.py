"""
Manifest coverage tests: every item declared in install-manifest.json must appear
in the ag-tregistry artifact store after an import. This is the parity guard — if
agent-architecture adds or removes an agent, MCP, or skill, these tests fail until
the import is re-run (or the manifest change is intentional).
"""
import json

import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import create_app


@pytest.fixture(scope="module")
def client_with_import():
    client = TestClient(create_app())
    resp = client.post("/api/imports/agent-architecture")
    assert resp.status_code == 200, f"import failed: {resp.text}"
    return client


@pytest.fixture(scope="module")
def manifest() -> dict:
    path = settings.agent_install_root / "install-manifest.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_all_manifest_agents_imported(client_with_import, manifest):
    manifest_agents = set(manifest.get("agents", []))
    assert manifest_agents, "manifest has no agents — check install-manifest.json"

    stored = {item["name"] for item in client_with_import.get("/api/artifacts", params={"kind": "agent"}).json()}
    missing = manifest_agents - stored
    assert not missing, f"agents in manifest but not imported: {sorted(missing)}"


def test_all_manifest_skills_imported(client_with_import, manifest):
    manifest_skills = set(manifest.get("skills", []))
    assert manifest_skills, "manifest has no skills — check install-manifest.json"

    stored = {item["name"] for item in client_with_import.get("/api/artifacts", params={"kind": "skill"}).json()}
    missing = manifest_skills - stored
    assert not missing, f"skills in manifest but not imported: {sorted(missing)}"


def test_all_manifest_mcps_imported(client_with_import, manifest):
    manifest_mcps = set(manifest.get("mcps", []))
    stored = {item["name"] for item in client_with_import.get("/api/artifacts", params={"kind": "mcp_server"}).json()}
    missing = manifest_mcps - stored
    assert not missing, f"MCPs in manifest but not imported: {sorted(missing)}"


def test_no_extra_artifacts_beyond_manifest(client_with_import, manifest):
    """Guard against ghost artifacts that exist in the store but not in manifest."""
    manifest_agents = set(manifest.get("agents", []))
    manifest_skills = set(manifest.get("skills", []))
    manifest_mcps = set(manifest.get("mcps", []))

    stored_agents = {item["name"] for item in client_with_import.get("/api/artifacts", params={"kind": "agent"}).json()}
    stored_skills = {item["name"] for item in client_with_import.get("/api/artifacts", params={"kind": "skill"}).json()}
    stored_mcps = {
        item["name"] for item in client_with_import.get("/api/artifacts", params={"kind": "mcp_server"}).json()
    }

    extra_agents = stored_agents - manifest_agents
    extra_skills = stored_skills - manifest_skills
    extra_mcps = stored_mcps - manifest_mcps

    assert not extra_agents, f"agents in store but not in manifest: {sorted(extra_agents)}"
    assert not extra_skills, f"skills in store but not in manifest: {sorted(extra_skills)}"
    assert not extra_mcps, f"MCPs in store but not in manifest: {sorted(extra_mcps)}"


def test_manifest_version_matches_stored_artifact_versions(client_with_import, manifest):
    expected_version = manifest.get("version", "latest")
    assert expected_version != "latest", "manifest should have a real version, not 'latest'"

    for kind in ("agent", "skill", "mcp_server"):
        stored = client_with_import.get("/api/artifacts", params={"kind": kind}).json()
        wrong = [item["name"] for item in stored if item["version"] != expected_version]
        assert not wrong, f"{kind} artifacts with wrong version (want {expected_version!r}): {wrong}"


def test_adapter_skills_imported_as_skills(client_with_import, manifest):
    """adapter-* entries in manifest.skills land as kind=skill, not a separate kind."""
    manifest_skills = set(manifest.get("skills", []))
    adapters_in_manifest = {s for s in manifest_skills if s.startswith("adapter-")}
    assert adapters_in_manifest, "expected adapter-* skills in manifest"

    stored = {item["name"] for item in client_with_import.get("/api/artifacts", params={"kind": "skill"}).json()}
    missing = adapters_in_manifest - stored
    assert not missing, f"adapter skills missing from store: {sorted(missing)}"


def test_import_summary_counts_match_manifest(client_with_import, manifest):
    summary = client_with_import.post("/api/imports/agent-architecture").json()
    assert summary["agents"] == len(manifest.get("agents", []))
    assert summary["mcps"] == len(manifest.get("mcps", []))
