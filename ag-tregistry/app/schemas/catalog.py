from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class ResponseMetadata(BaseModel):
    next_cursor: str | None = Field(default=None, alias="nextCursor")

    model_config = ConfigDict(populate_by_name=True)


class ListServersResponse(BaseModel):
    servers: list[dict[str, Any]]
    metadata: ResponseMetadata


class ListSkillsResponse(BaseModel):
    skills: list[dict[str, Any]]
    metadata: ResponseMetadata


class ListAgentsResponse(BaseModel):
    agents: list[dict[str, Any]]
    metadata: ResponseMetadata


class ListPromptsResponse(BaseModel):
    prompts: list[dict[str, Any]]
    metadata: ResponseMetadata


class DeploymentTargetRef(BaseModel):
    kind: str
    name: str
    tag: str = "latest"


class DeploymentRuntimeRef(BaseModel):
    kind: str = "Runtime"
    name: str = "local"


class DeploymentCondition(BaseModel):
    type: str
    status: str
    reason: str
    message: str = ""
    last_transition_time: str = Field(alias="lastTransitionTime")

    model_config = ConfigDict(populate_by_name=True)


class DeploymentStatus(BaseModel):
    conditions: list[DeploymentCondition]


class DeploymentMetadata(BaseModel):
    name: str
    namespace: str = "default"
    created_at: str = Field(alias="createdAt")
    annotations: dict[str, str] = Field(default_factory=dict)

    model_config = ConfigDict(populate_by_name=True)


class DeploymentSpec(BaseModel):
    target_ref: DeploymentTargetRef = Field(alias="targetRef")
    runtime_ref: DeploymentRuntimeRef = Field(alias="runtimeRef")
    desired_state: str = Field(default="deployed", alias="desiredState")
    env: dict[str, str] = Field(default_factory=dict)
    runtime_config: dict[str, Any] = Field(default_factory=dict, alias="runtimeConfig")

    model_config = ConfigDict(populate_by_name=True)


class DeploymentEnvelope(BaseModel):
    api_version: str = Field(default="agentregistry/v1alpha1", alias="apiVersion")
    kind: str = "Deployment"
    metadata: DeploymentMetadata
    spec: DeploymentSpec
    status: DeploymentStatus

    model_config = ConfigDict(populate_by_name=True)


class ListDeploymentsResponse(BaseModel):
    items: list[DeploymentEnvelope]


class DeploymentCreate(BaseModel):
    resource_type: Literal["agent", "mcp"] = Field(alias="resourceType")
    resource_name: str = Field(min_length=1, max_length=128, alias="resourceName")
    tag: str = "latest"
    runtime_id: str = Field(default="local", alias="runtimeId")
    namespace: str = "default"

    model_config = ConfigDict(populate_by_name=True)


class DeploymentDeleteResponse(BaseModel):
    message: str


class DeploymentRecordRead(BaseModel):
    id: str
    resource_type: str
    resource_name: str
    tag: str
    runtime_id: str
    namespace: str
    status: str
    origin: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
