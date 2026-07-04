export type RuntimeSummary = {
  current_runtime: string;
  runtime_bridged: boolean;
  status_message: string;
  configured_hosts: string[];
  installed_agents: number;
  installed_skills: number;
  configured_mcps: number;
  install_manifest_path: string;
  settings_path: string;
};

export type RuntimeAgent = {
  id: string;
  description: string;
  source_path: string;
  installed: boolean;
  enabled: boolean;
  indexed: boolean;
  callable_hosts: string[];
  active_runtime: string;
  callable_now: boolean;
};

export type RuntimeSkill = {
  id: string;
  description: string;
  source_path: string;
  owners: string[];
  installed: boolean;
  indexed: boolean;
  callable_hosts: string[];
  active_runtime: string;
  callable_now: boolean;
};

export type RuntimeMcp = {
  id: string;
  command: string;
  args: string[];
  env_refs: string[];
  configured: boolean;
  installed: boolean;
  running: boolean;
  connected_to_current_runtime: boolean;
  callable_hosts: string[];
};

export type RuntimeHost = {
  id: string;
  configured: boolean;
  artifact_path: string;
  installed_artifact: boolean;
  supported_by_current_runtime: boolean;
  callable_now: boolean;
};

export type RuntimeSnapshot = {
  summary: RuntimeSummary;
  agents: RuntimeAgent[];
  skills: RuntimeSkill[];
  mcps: RuntimeMcp[];
  hosts: RuntimeHost[];
};

export type ResponseMeta = {
  nextCursor: string | null;
};

export type ServerResponse = {
  server: {
    name: string;
    title?: string;
    description?: string;
    tag: string;
    _meta?: Record<string, unknown>;
  };
  _meta?: Record<string, unknown>;
};

export type SkillResponse = {
  skill: {
    name: string;
    title?: string;
    description?: string;
    tag: string;
    source?: string;
    owners?: string[];
  };
  _meta?: Record<string, unknown>;
};

export type AgentResponse = {
  agent: {
    name: string;
    description?: string;
    modelProvider?: string;
    modelName?: string;
    tag: string;
    skills?: string[];
    source?: string;
  };
  _meta?: Record<string, unknown>;
};

export type PromptResponse = {
  prompt: {
    name: string;
    description?: string;
    content?: string;
    tag: string;
    source?: string;
  };
  _meta?: Record<string, unknown>;
};

export type ListServersResponse = {
  servers: ServerResponse[];
  metadata: ResponseMeta;
};

export type ListSkillsResponse = {
  skills: SkillResponse[];
  metadata: ResponseMeta;
};

export type ListAgentsResponse = {
  agents: AgentResponse[];
  metadata: ResponseMeta;
};

export type ListPromptsResponse = {
  prompts: PromptResponse[];
  metadata: ResponseMeta;
};

export type DeploymentEnvelope = {
  apiVersion: string;
  kind: "Deployment";
  metadata: {
    name: string;
    namespace: string;
    createdAt: string;
    annotations?: Record<string, string>;
  };
  spec: {
    targetRef: {
      kind: string;
      name: string;
      tag: string;
    };
    runtimeRef: {
      kind: string;
      name: string;
    };
    desiredState: string;
    env: Record<string, string>;
    runtimeConfig: Record<string, unknown>;
  };
  status: {
    conditions: Array<{
      type: string;
      status: string;
      reason: string;
      message: string;
      lastTransitionTime: string;
    }>;
  };
};

export type ListDeploymentsResponse = {
  items: DeploymentEnvelope[];
};

export type DeploymentCreate = {
  resourceType: "agent" | "mcp";
  resourceName: string;
  tag?: string;
  runtimeId?: string;
  namespace?: string;
};
