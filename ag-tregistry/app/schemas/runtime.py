from pydantic import BaseModel, Field


class RuntimeSummary(BaseModel):
    current_runtime: str
    runtime_bridged: bool
    status_message: str
    configured_hosts: list[str] = Field(default_factory=list)
    installed_agents: int
    installed_skills: int
    configured_mcps: int
    install_manifest_path: str
    settings_path: str


class RuntimeAgentRead(BaseModel):
    id: str
    description: str = ""
    source_path: str
    installed: bool
    enabled: bool
    indexed: bool
    callable_hosts: list[str] = Field(default_factory=list)
    active_runtime: str
    callable_now: bool


class RuntimeSkillRead(BaseModel):
    id: str
    description: str = ""
    source_path: str
    owners: list[str] = Field(default_factory=list)
    installed: bool
    indexed: bool
    callable_hosts: list[str] = Field(default_factory=list)
    active_runtime: str
    callable_now: bool


class RuntimeMcpRead(BaseModel):
    id: str
    command: str
    args: list[str] = Field(default_factory=list)
    env_refs: list[str] = Field(default_factory=list)
    configured: bool
    installed: bool
    running: bool
    connected_to_current_runtime: bool
    callable_hosts: list[str] = Field(default_factory=list)


class RuntimeHostRead(BaseModel):
    id: str
    configured: bool
    artifact_path: str
    installed_artifact: bool
    supported_by_current_runtime: bool
    callable_now: bool


class RuntimeSnapshot(BaseModel):
    summary: RuntimeSummary
    agents: list[RuntimeAgentRead]
    skills: list[RuntimeSkillRead]
    mcps: list[RuntimeMcpRead]
    hosts: list[RuntimeHostRead]
