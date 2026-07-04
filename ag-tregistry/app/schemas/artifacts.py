from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

ArtifactKind = Literal["agent", "skill", "prompt", "mcp_server", "deployment"]


class ArtifactCreate(BaseModel):
    id: str = Field(min_length=1, max_length=128)
    kind: ArtifactKind
    name: str = Field(min_length=1, max_length=128)
    version: str = "latest"
    description: str = ""
    source: str = "manual"


class ArtifactRead(ArtifactCreate):
    created_at: datetime

    model_config = {"from_attributes": True}


class ImportSummary(BaseModel):
    imported: int
    agents: int
    skills: int
    mcps: int = 0
    version: str = "latest"
    source_registry: str
