from fastapi.testclient import TestClient

from app.main import create_app

client = TestClient(create_app())


def test_v0_inventory_routes_expose_vendored_runtime():
    servers = client.get("/api/v0/servers")
    skills = client.get("/api/v0/skills")
    agents = client.get("/api/v0/agents")
    prompts = client.get("/api/v0/prompts")

    assert servers.status_code == 200
    assert skills.status_code == 200
    assert agents.status_code == 200
    assert prompts.status_code == 200

    assert isinstance(servers.json()["servers"], list)
    assert any(item["skill"]["name"] == "spec" for item in skills.json()["skills"])
    assert any(item["agent"]["name"] == "orchestrate" for item in agents.json()["agents"])
    assert any(item["prompt"]["name"] == "codex" for item in prompts.json()["prompts"])


def test_artifact_post_upsert():
    payload = {"id": "test:unit-artifact", "kind": "skill", "name": "unit-artifact", "version": "1.0.0"}
    created = client.post("/api/artifacts", json=payload)
    assert created.status_code == 200
    assert created.json()["name"] == "unit-artifact"

    payload["version"] = "2.0.0"
    updated = client.post("/api/artifacts", json=payload)
    assert updated.status_code == 200
    assert updated.json()["version"] == "2.0.0"

    listed = client.get("/api/artifacts", params={"kind": "skill"})
    ids = [item["id"] for item in listed.json()]
    assert "test:unit-artifact" in ids


def test_deployment_create_list_delete_round_trip():
    created = client.post(
        "/api/v0/deployments",
        json={
            "resourceType": "agent",
            "resourceName": "swe",
            "tag": "latest",
            "runtimeId": "local",
            "namespace": "default",
        },
    )
    assert created.status_code == 200
    deployment_name = created.json()["item"]["metadata"]["name"]

    listed = client.get("/api/v0/deployments", params={"namespace": "all"})
    assert listed.status_code == 200
    items = listed.json()["items"]
    assert any(item["spec"]["targetRef"]["name"] == "swe" for item in items)

    removed = client.delete(f"/api/v0/deployments/{deployment_name}")
    assert removed.status_code == 200

    listed_after = client.get("/api/v0/deployments", params={"namespace": "all"})
    assert all(item["metadata"]["name"] != deployment_name for item in listed_after.json()["items"])
