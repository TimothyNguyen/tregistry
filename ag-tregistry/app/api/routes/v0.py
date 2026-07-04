from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.catalog import (
    DeploymentCreate,
    DeploymentDeleteResponse,
    ListAgentsResponse,
    ListDeploymentsResponse,
    ListPromptsResponse,
    ListServersResponse,
    ListSkillsResponse,
    ResponseMetadata,
)
from app.services.catalog import CatalogService

router = APIRouter(prefix="/v0", tags=["v0"])


@router.get("/servers", response_model=ListServersResponse)
def list_servers() -> ListServersResponse:
    service = CatalogService()
    return ListServersResponse(servers=service.list_servers(), metadata=ResponseMetadata(nextCursor=None))


@router.get("/skills", response_model=ListSkillsResponse)
def list_skills() -> ListSkillsResponse:
    service = CatalogService()
    return ListSkillsResponse(skills=service.list_skills(), metadata=ResponseMetadata(nextCursor=None))


@router.get("/agents", response_model=ListAgentsResponse)
def list_agents() -> ListAgentsResponse:
    service = CatalogService()
    return ListAgentsResponse(agents=service.list_agents(), metadata=ResponseMetadata(nextCursor=None))


@router.get("/prompts", response_model=ListPromptsResponse)
def list_prompts() -> ListPromptsResponse:
    service = CatalogService()
    return ListPromptsResponse(prompts=service.list_prompts(), metadata=ResponseMetadata(nextCursor=None))


@router.get("/deployments", response_model=ListDeploymentsResponse)
def list_deployments(
    namespace: str = Query(default="default"),
    session: Session = Depends(get_session),
) -> ListDeploymentsResponse:
    return ListDeploymentsResponse(items=CatalogService(session).list_deployments(namespace=namespace))


@router.post("/deployments", response_model=dict)
def create_deployment(payload: DeploymentCreate, session: Session = Depends(get_session)) -> dict:
    deployment = CatalogService(session).create_deployment(payload)
    return {"item": deployment.model_dump(by_alias=True)}


@router.delete("/deployments/{name}", response_model=DeploymentDeleteResponse)
def delete_deployment(
    name: str,
    namespace: str = Query(default="default"),
    session: Session = Depends(get_session),
) -> DeploymentDeleteResponse:
    return CatalogService(session).delete_deployment(name=name, namespace=namespace)
