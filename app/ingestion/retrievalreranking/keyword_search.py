from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import SessionLocal
from app.models.chunk import Chunk


class KeywordSearch:
    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[tuple[Chunk, float]]:
        db = SessionLocal()

        try:
            statement = (
                select(Chunk)
                .options(selectinload(Chunk.file))
                .where(Chunk.content.ilike(f"%{query}%"))
                .limit(top_k)
            )

            chunks = db.execute(statement).scalars().all()

            return [
                (chunk, 1.0)
                for chunk in chunks
            ]

        finally:
            db.close()