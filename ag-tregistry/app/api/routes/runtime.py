from fastapi import APIRouter

from app.schemas.runtime import (
    RuntimeAgentRead,
    RuntimeHostRead,
    RuntimeMcpRead,
    RuntimeSkillRead,
    RuntimeSnapshot,
    RuntimeSummary,
)
from app.services.runtime_inventory import build_runtime_snapshot

router = APIRouter(prefix="/runtime", tags=["runtime"])


@router.get("/snapshot", response_model=RuntimeSnapshot)
def runtime_snapshot() -> RuntimeSnapshot:
    return build_runtime_snapshot()


@router.get("/summary", response_model=RuntimeSummary)
def runtime_summary() -> RuntimeSummary:
    return build_runtime_snapshot().summary


@router.get("/agents", response_model=list[RuntimeAgentRead])
def runtime_agents() -> list[RuntimeAgentRead]:
    return build_runtime_snapshot().agents


@router.get("/skills", response_model=list[RuntimeSkillRead])
def runtime_skills() -> list[RuntimeSkillRead]:
    return build_runtime_snapshot().skills


@router.get("/mcps", response_model=list[RuntimeMcpRead])
def runtime_mcps() -> list[RuntimeMcpRead]:
    return build_runtime_snapshot().mcps


@router.get("/hosts", response_model=list[RuntimeHostRead])
def runtime_hosts() -> list[RuntimeHostRead]:
    return build_runtime_snapshot().hosts
