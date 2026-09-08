from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import SessionLocal
from app.ingestion.embeddings.embedding_service import EmbeddingService
from app.models.chunk import Chunk


class SemanticSearch:
    def __init__(self):
        self.embedding_service = EmbeddingService()

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[tuple[Chunk, float]]:
        query_embedding = self.embedding_service.embed(query)

        db = SessionLocal()

        try:
            distance = Chunk.embedding.cosine_distance(query_embedding)

            statement = (
                select(Chunk)
                .options(selectinload(Chunk.file))
                .add_columns(distance)
                .order_by(distance)
                .limit(top_k)
            )

            results = db.execute(statement).all()

            return [
                (chunk, 1 - distance_value)
                for chunk, distance_value in results
            ]

        finally:
            db.close()