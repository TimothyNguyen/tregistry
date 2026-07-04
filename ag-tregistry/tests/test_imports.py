from fastapi.testclient import TestClient

from app.main import create_app

client = TestClient(create_app())


def test_agent_architecture_import_summary():
    body = client.post("/api/imports/agent-architecture").json()
    assert body["imported"] > 0
    assert body["agents"] > 0
    assert body["skills"] > 0
    assert body["mcps"] >= 0
    assert body["version"] != ""
    assert body["version"] != "latest"


def test_agent_architecture_import_stores_agents():
    client.post("/api/imports/agent-architecture")
    agents = client.get("/api/artifacts", params={"kind": "agent"}).json()
    names = {item["name"] for item in agents}
    assert "swe" in names
    assert "orchestrate" in names
    assert "security" in names


def test_agent_architecture_import_stores_skills():
    client.post("/api/imports/agent-architecture")
    skills = client.get("/api/artifacts", params={"kind": "skill"}).json()
    names = {item["name"] for item in skills}
    assert "spec" in names
    assert "review" in names


def test_agent_architecture_import_stores_mcps():
    import json

    from app.core.config import settings

    manifest = json.loads((settings.agent_install_root / "install-manifest.json").read_text())
    expected = set(manifest.get("mcps", []))
    client.post("/api/imports/agent-architecture")
    mcps = client.get("/api/artifacts", params={"kind": "mcp_server"}).json()
    names = {item["name"] for item in mcps}
    assert names == expected


def test_agent_architecture_import_version_propagates_to_artifacts():
    summary = client.post("/api/imports/agent-architecture").json()
    imported_version = summary["version"]
    artifacts = client.get("/api/artifacts", params={"kind": "agent"}).json()
    assert all(item["version"] == imported_version for item in artifacts)


def test_agent_architecture_import_is_idempotent():
    first = client.post("/api/imports/agent-architecture").json()
    second = client.post("/api/imports/agent-architecture").json()
    assert first["imported"] == second["imported"]
    assert first["agents"] == second["agents"]
    assert first["skills"] == second["skills"]
    assert first["mcps"] == second["mcps"]

    agents_after = client.get("/api/artifacts", params={"kind": "agent"}).json()
    agent_ids = [item["id"] for item in agents_after]
    assert len(agent_ids) == len(set(agent_ids))
