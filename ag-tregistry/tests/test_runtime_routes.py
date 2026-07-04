from fastapi.testclient import TestClient

from app.main import create_app

client = TestClient(create_app())


def test_runtime_snapshot_route_exposes_inventory():
    response = client.get("/api/runtime/snapshot")
    assert response.status_code == 200

    body = response.json()
    assert body["summary"]["installed_agents"] >= 10
    assert body["summary"]["configured_mcps"] >= 0
    assert any(agent["id"] == "swe" for agent in body["agents"])
    assert any(skill["id"] == "review" for skill in body["skills"])
    assert isinstance(body["mcps"], list)
    assert any(host["id"] == "claude" for host in body["hosts"])


def test_runtime_summary_and_agents_routes():
    summary = client.get("/api/runtime/summary")
    agents = client.get("/api/runtime/agents")

    assert summary.status_code == 200
    assert agents.status_code == 200
    assert "status_message" in summary.json()
    assert any(item["id"] == "security" for item in agents.json())


def test_runtime_skills_route():
    resp = client.get("/api/runtime/skills")
    assert resp.status_code == 200
    assert any(item["id"] == "spec" for item in resp.json())


def test_runtime_mcps_route():
    resp = client.get("/api/runtime/mcps")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_runtime_hosts_route():
    resp = client.get("/api/runtime/hosts")
    assert resp.status_code == 200
    assert any(item["id"] == "claude" for item in resp.json())
