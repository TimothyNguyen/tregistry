import type {
  DeploymentCreate,
  DeploymentEnvelope,
  ListAgentsResponse,
  ListDeploymentsResponse,
  ListPromptsResponse,
  ListServersResponse,
  ListSkillsResponse,
  RuntimeSnapshot,
} from "./types";

const API_BASE = "http://127.0.0.1:8000/api";

async function parseJson<T>(response: Response, fallback: string): Promise<T> {
  if (!response.ok) {
    throw new Error(fallback);
  }
  return response.json() as Promise<T>;
}

export async function importAgentArchitecture(): Promise<void> {
  const response = await fetch(`${API_BASE}/imports/agent-architecture`, { method: "POST" });
  if (!response.ok) {
    throw new Error("Import failed");
  }
}

export async function fetchRuntimeSnapshot(): Promise<RuntimeSnapshot> {
  const response = await fetch(`${API_BASE}/runtime/snapshot`);
  return parseJson<RuntimeSnapshot>(response, "Runtime snapshot fetch failed");
}

export async function fetchServers(): Promise<ListServersResponse> {
  const response = await fetch(`${API_BASE}/v0/servers`);
  return parseJson<ListServersResponse>(response, "Server fetch failed");
}

export async function fetchSkills(): Promise<ListSkillsResponse> {
  const response = await fetch(`${API_BASE}/v0/skills`);
  return parseJson<ListSkillsResponse>(response, "Skill fetch failed");
}

export async function fetchAgents(): Promise<ListAgentsResponse> {
  const response = await fetch(`${API_BASE}/v0/agents`);
  return parseJson<ListAgentsResponse>(response, "Agent fetch failed");
}

export async function fetchPrompts(): Promise<ListPromptsResponse> {
  const response = await fetch(`${API_BASE}/v0/prompts`);
  return parseJson<ListPromptsResponse>(response, "Prompt fetch failed");
}

export async function fetchDeployments(namespace = "all"): Promise<DeploymentEnvelope[]> {
  const url = new URL(`${API_BASE}/v0/deployments`);
  url.searchParams.set("namespace", namespace);
  const response = await fetch(url);
  const body = await parseJson<ListDeploymentsResponse>(response, "Deployment fetch failed");
  return body.items;
}

export async function deployResource(payload: DeploymentCreate): Promise<DeploymentEnvelope> {
  const response = await fetch(`${API_BASE}/v0/deployments`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const body = await parseJson<{ item: DeploymentEnvelope }>(response, "Deploy failed");
  return body.item;
}

export async function deleteDeployment(name: string, namespace = "default"): Promise<void> {
  const url = new URL(`${API_BASE}/v0/deployments/${name}`);
  url.searchParams.set("namespace", namespace);
  const response = await fetch(url, { method: "DELETE" });
  if (!response.ok) {
    throw new Error("Delete deployment failed");
  }
}
