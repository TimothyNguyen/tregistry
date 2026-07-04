from collections.abc import Sequence

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.models import Artifact
from app.db.session import get_session
from app.schemas.artifacts import ArtifactCreate, ArtifactRead
from app.services.artifacts import ArtifactService

router = APIRouter(prefix="/artifacts", tags=["artifacts"])


@router.get("", response_model=list[ArtifactRead])
def list_artifacts(
    kind: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> Sequence[Artifact]:
    return ArtifactService(session).list_artifacts(kind=kind)


@router.post("", response_model=ArtifactRead)
def upsert_artifact(payload: ArtifactCreate, session: Session = Depends(get_session)) -> Artifact:
    return ArtifactService(session).upsert_artifact(payload)
