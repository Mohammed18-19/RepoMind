from app.database import SessionLocal
from app.models.chunk import Chunk
from app.ingestion.embeddings.embedding_service import EmbeddingService


class ChunkStorage:
    def __init__(self):
        self.embedding_service = EmbeddingService()

    def save_chunks(self, file_id: int, chunks: list[dict]) -> None:
        db = SessionLocal()

        try:
            for chunk_data in chunks:
                embedding = self.embedding_service.embed(
                    chunk_data["content"]
                )

                chunk = Chunk(
                    file_id=file_id,
                    content=chunk_data["content"],
                    embedding=embedding,
                    start_line=chunk_data["start_line"],
                    end_line=chunk_data["end_line"],
                )

                db.add(chunk)

            db.commit()

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()