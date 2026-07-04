from collections.abc import Sequence

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.db.models import Artifact
from app.schemas.artifacts import ArtifactCreate


class ArtifactService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_artifacts(self, kind: str | None = None) -> Sequence[Artifact]:
        stmt = select(Artifact).order_by(Artifact.kind, Artifact.name)
        if kind:
            stmt = stmt.where(Artifact.kind == kind)
        return self.session.scalars(stmt).all()

    def upsert_artifact(self, payload: ArtifactCreate) -> Artifact:
        artifact = self.session.get(Artifact, payload.id)
        if artifact is None:
            artifact = Artifact(**payload.model_dump())
            self.session.add(artifact)
        else:
            for key, value in payload.model_dump().items():
                setattr(artifact, key, value)
        self.session.commit()
        self.session.refresh(artifact)
        return artifact

    def replace_by_kinds(self, artifacts: list[ArtifactCreate], kinds: list[str]) -> None:
        """Delete all artifacts of the given kinds then insert the provided list.

        This makes import a sync operation rather than an additive upsert, so
        stale entries from a previous import do not linger after the source changes.
        """
        if kinds:
            self.session.execute(delete(Artifact).where(Artifact.kind.in_(kinds)))
        for payload in artifacts:
            self.session.add(Artifact(**payload.model_dump()))
        self.session.commit()
