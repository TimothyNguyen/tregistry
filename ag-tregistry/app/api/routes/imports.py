from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_session
from app.schemas.artifacts import ImportSummary
from app.services.artifacts import ArtifactService
from imports.agent_architecture.registry import import_registry

router = APIRouter(prefix="/imports", tags=["imports"])


@router.post("/agent-architecture")
def import_agent_architecture(session: Session = Depends(get_session)) -> ImportSummary:
    registry_path = settings.agent_architecture_root / "generated" / "registry.json"
    manifest_path = settings.agent_install_root / "install-manifest.json"
    artifacts, summary = import_registry(registry_path, manifest_path=manifest_path)
    service = ArtifactService(session)
    service.replace_by_kinds(artifacts, kinds=["agent", "skill", "mcp_server"])
    return summary
