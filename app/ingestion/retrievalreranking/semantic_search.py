from sqlalchemy import select

from app.database import SessionLocal
from app.ingestion.embeddings.embedding_service import EmbeddingService
from app.models.chunk import Chunk


class SemanticSearch:
    def __init__(self):
        self.embedding_service = EmbeddingService()

    def search(self, query: str, top_k: int = 5) -> list[Chunk]:
        query_embedding = self.embedding_service.embed(query)

        db = SessionLocal()

        try:
            distance = Chunk.embedding.cosine_distance(query_embedding)

            statement = (
                select(Chunk)
                .order_by(distance)
                .limit(top_k)
            )

            return db.execute(statement).scalars().all()

        finally:
            db.close()