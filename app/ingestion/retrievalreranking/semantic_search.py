from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import SessionLocal
from app.ingestion.embeddings.embedding_service import EmbeddingService
from app.models.chunk import Chunk
from app.models.file import File


class SemanticSearch:
    def __init__(self):
        self.embedding_service = EmbeddingService()

    def search(
        self,
        query: str,
        top_k: int = 30,
        repository_id: int | None = None,
    ) -> list[tuple[Chunk, float]]:
        query_embedding = self.embedding_service.embed(query)

        db = SessionLocal()

        try:
            distance = Chunk.embedding.cosine_distance(
                query_embedding
            )

            statement = (
                select(Chunk)
                .join(
                    File,
                    Chunk.file_id == File.id,
                )
                .options(
                    selectinload(Chunk.file)
                )
                .add_columns(distance)
                .order_by(distance)
                .limit(top_k)
            )

            if repository_id is not None:
                statement = statement.where(
                    File.repository_id == repository_id
                )

            results = db.execute(statement).all()

            return [
                (chunk, 1 - float(distance_value))
                for chunk, distance_value in results
            ]

        finally:
            db.close()
