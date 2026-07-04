import { useEffect, useState } from "react";

import {
  deleteDeployment,
  deployResource,
  fetchAgents,
  fetchDeployments,
  fetchPrompts,
  fetchRuntimeSnapshot,
  fetchServers,
  fetchSkills,
  importAgentArchitecture,
} from "./api";
import type {
  AgentResponse,
  DeploymentEnvelope,
  PromptResponse,
  RuntimeSnapshot,
  ServerResponse,
  SkillResponse,
} from "./types";

type View = "catalog" | "deployed";
type Tab = "servers" | "skills" | "agents" | "prompts";

const tabs: Tab[] = ["servers", "skills", "agents", "prompts"];

export function App() {
  const [view, setView] = useState<View>("catalog");
  const [tab, setTab] = useState<Tab>("servers");
  const [runtime, setRuntime] = useState<RuntimeSnapshot | null>(null);
  const [servers, setServers] = useState<ServerResponse[]>([]);
  const [skills, setSkills] = useState<SkillResponse[]>([]);
  const [agents, setAgents] = useState<AgentResponse[]>([]);
  const [prompts, setPrompts] = useState<PromptResponse[]>([]);
  const [deployments, setDeployments] = useState<DeploymentEnvelope[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [query, setQuery] = useState("");

  async function loadAll() {
    setBusy(true);
    setError(null);
    try {
      const [runtimeSnapshot, serverData, skillData, agentData, promptData, deploymentData] = await Promise.all([
        fetchRuntimeSnapshot(),
        fetchServers(),
        fetchSkills(),
        fetchAgents(),
        fetchPrompts(),
        fetchDeployments(),
      ]);
      setRuntime(runtimeSnapshot);
      setServers(serverData.servers);
      setSkills(skillData.skills);
      setAgents(agentData.agents);
      setPrompts(promptData.prompts);
      setDeployments(deploymentData);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Load failed");
    } finally {
      setBusy(false);
    }
  }

  useEffect(() => {
    void loadAll();
  }, []);

  const filteredServers = servers.filter(({ server }) => matchesQuery(query, [server.name, server.title, server.description]));
  const filteredSkills = skills.filter(({ skill }) => matchesQuery(query, [skill.name, skill.title, skill.description, ...(skill.owners ?? [])]));
  const filteredAgents = agents.filter(({ agent }) => matchesQuery(query, [agent.name, agent.description, agent.modelProvider, ...(agent.skills ?? [])]));
  const filteredPrompts = prompts.filter(({ prompt }) => matchesQuery(query, [prompt.name, prompt.description, prompt.content]));
  const filteredDeployments = deployments.filter((item) =>
    matchesQuery(query, [item.metadata.name, item.spec.targetRef.name, item.spec.targetRef.kind, item.spec.runtimeRef.name]),
  );

  return (
    <main className="page-shell">
      <header className="masthead">
        <div>
          <p className="eyebrow">ag-tregistry</p>
          <h1>Vendored agent runtime, exposed as registry.</h1>
          <p className="lede">
            `tstack` stays packaging source. `ag-tregistry` surfaces installed agents, skills, prompts, MCP servers,
            and managed deployments.
          </p>
        </div>
        <div className="hero-actions">
          <button
            className="primary"
            disabled={busy}
            onClick={async () => {
              setBusy(true);
              try {
                await importAgentArchitecture();
                await loadAll();
              } finally {
                setBusy(false);
              }
            }}
          >
            {busy ? "Syncing..." : "Sync Vendored Registry"}
          </button>
        </div>
      </header>

      {runtime ? (
        <section className="status-strip">
          <div>
            <p className="meta-label">Runtime</p>
            <strong>{runtime.summary.status_message}</strong>
          </div>
          <div className="status-grid">
            <span>{runtime.summary.installed_agents} agents</span>
            <span>{runtime.summary.installed_skills} skills</span>
            <span>{runtime.summary.configured_mcps} MCPs</span>
            <span>hosts: {runtime.summary.configured_hosts.join(", ") || "none"}</span>
          </div>
        </section>
      ) : null}

      <nav className="view-switch">
        <button className={view === "catalog" ? "switch active" : "switch"} onClick={() => setView("catalog")}>
          Catalog
        </button>
        <button className={view === "deployed" ? "switch active" : "switch"} onClick={() => setView("deployed")}>
          Deployed
        </button>
      </nav>

      <section className="toolbar">
        {view === "catalog" ? (
          <div className="tab-row">
            {tabs.map((item) => (
              <button key={item} className={tab === item ? "pill active" : "pill"} onClick={() => setTab(item)}>
                {item}
                <span className="count">{countForTab(item, servers, skills, agents, prompts)}</span>
              </button>
            ))}
          </div>
        ) : (
          <div className="tab-row">
            <span className="pill active">deployments <span className="count">{deployments.length}</span></span>
          </div>
        )}
        <input
          className="search"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder={view === "catalog" ? `Search ${tab}...` : "Search deployments..."}
        />
      </section>

      {error ? <p className="empty">{error}</p> : null}

      {view === "catalog" ? (
        <section className="registry-list">
          {tab === "servers" &&
            filteredServers.map((item) => (
              <article key={item.server.name} className="registry-row">
                <div>
                  <p className="meta-label">MCP Server</p>
                  <h2>{item.server.title || item.server.name}</h2>
                  <p>{item.server.description}</p>
                </div>
                <div className="row-actions">
                  <code>{item.server.tag}</code>
                  <button
                    className="secondary"
                    onClick={async () => {
                      await deployResource({ resourceType: "mcp", resourceName: item.server.name });
                      await loadAll();
                      setView("deployed");
                    }}
                  >
                    Deploy
                  </button>
                </div>
              </article>
            ))}

          {tab === "skills" &&
            filteredSkills.map((item) => (
              <article key={item.skill.name} className="registry-row">
                <div>
                  <p className="meta-label">Skill</p>
                  <h2>{item.skill.title || item.skill.name}</h2>
                  <p>{item.skill.description}</p>
                </div>
                <div className="row-side">
                  <code>{item.skill.tag}</code>
                  <span>{(item.skill.owners ?? []).join(", ") || "no owners"}</span>
                </div>
              </article>
            ))}

          {tab === "agents" &&
            filteredAgents.map((item) => (
              <article key={item.agent.name} className="registry-row">
                <div>
                  <p className="meta-label">Agent</p>
                  <h2>{item.agent.name}</h2>
                  <p>{item.agent.description}</p>
                </div>
                <div className="row-actions">
                  <code>{item.agent.tag}</code>
                  <button
                    className="secondary"
                    onClick={async () => {
                      await deployResource({ resourceType: "agent", resourceName: item.agent.name });
                      await loadAll();
                      setView("deployed");
                    }}
                  >
                    Deploy
                  </button>
                </div>
              </article>
            ))}

          {tab === "prompts" &&
            filteredPrompts.map((item) => (
              <article key={item.prompt.name} className="registry-row">
                <div>
                  <p className="meta-label">Prompt</p>
                  <h2>{item.prompt.name}</h2>
                  <p>{item.prompt.description}</p>
                </div>
                <div className="row-side prompt-preview">
                  <code>{item.prompt.tag}</code>
                  <span>{truncate(item.prompt.content ?? "", 180)}</span>
                </div>
              </article>
            ))}

          {!busy && activeLength(tab, filteredServers, filteredSkills, filteredAgents, filteredPrompts) === 0 ? (
            <p className="empty">No matching entries.</p>
          ) : null}
        </section>
      ) : (
        <section className="registry-list">
          {filteredDeployments.map((item) => (
            <article key={`${item.metadata.namespace}/${item.metadata.name}`} className="registry-row">
              <div>
                <p className="meta-label">{item.spec.targetRef.kind}</p>
                <h2>{item.spec.targetRef.name}</h2>
                <p>
                  deployment `{item.metadata.name}` on runtime `{item.spec.runtimeRef.name}` in namespace `
                  {item.metadata.namespace}`
                </p>
              </div>
              <div className="row-actions">
                <code>{item.spec.targetRef.tag}</code>
                <button
                  className="danger"
                  onClick={async () => {
                    await deleteDeployment(item.metadata.name, item.metadata.namespace);
                    await loadAll();
                  }}
                >
                  Remove
                </button>
              </div>
            </article>
          ))}
          {!busy && filteredDeployments.length === 0 ? <p className="empty">No deployments yet.</p> : null}
        </section>
      )}
    </main>
  );
}

function matchesQuery(query: string, values: Array<string | undefined>): boolean {
  if (!query.trim()) {
    return true;
  }
  const needle = query.trim().toLowerCase();
  return values.some((value) => (value ?? "").toLowerCase().includes(needle));
}

function countForTab(
  tab: Tab,
  servers: ServerResponse[],
  skills: SkillResponse[],
  agents: AgentResponse[],
  prompts: PromptResponse[],
): number {
  if (tab === "servers") return servers.length;
  if (tab === "skills") return skills.length;
  if (tab === "agents") return agents.length;
  return prompts.length;
}

function activeLength(
  tab: Tab,
  servers: ServerResponse[],
  skills: SkillResponse[],
  agents: AgentResponse[],
  prompts: PromptResponse[],
): number {
  if (tab === "servers") return servers.length;
  if (tab === "skills") return skills.length;
  if (tab === "agents") return agents.length;
  return prompts.length;
}

function truncate(value: string, maxLength: number): string {
  if (value.length <= maxLength) {
    return value;
  }
  return `${value.slice(0, maxLength)}...`;
}
