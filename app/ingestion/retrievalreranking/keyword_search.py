import re

from sqlalchemy import (
    select,
    func,
    or_,
    case,
)
from sqlalchemy.orm import selectinload

from app.database import SessionLocal
from app.models.chunk import Chunk
from app.models.file import File


class KeywordSearch:
    def search(
        self,
        query: str,
        top_k: int = 30,
        repository_id: int | None = None,
    ) -> list[tuple[Chunk, float]]:

        db = SessionLocal()

        try:
            search_vector = func.to_tsvector(
                "english",
                Chunk.content,
            )

            search_query = func.plainto_tsquery(
                "english",
                query,
            )

            fts_rank = func.ts_rank(
                search_vector,
                search_query,
            )

            stopwords = {
                "how", "does", "what", "why", "when", "where",
                "can", "could", "would", "should",
                "the", "a", "an", "and", "or", "with",
                "for", "from", "into", "about", "this", "that",
                "is", "are", "was", "were", "be", "to", "of",
                "in", "on", "as", "by",
            }

            identifier_tokens = [
                token
                for token in re.findall(
                    r"[A-Za-z_][A-Za-z0-9_]{2,}",
                    query,
                )
                if token.lower() not in stopwords
            ]

            conditions = [
                search_vector.op("@@")(search_query)
            ]

            identifier_score = 0.0

            for token in identifier_tokens:
                conditions.append(
                    Chunk.content.ilike(
                        f"%{token}%"
                    )
                )

                identifier_score += case(
                    (
                        Chunk.content.ilike(
                            f"%{token}%"
                        ),
                        2.0,
                    ),
                    else_=0.0,
                )

            combined_score = (
                fts_rank + identifier_score
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
                .where(
                    or_(*conditions)
                )
                .add_columns(combined_score)
                .order_by(
                    combined_score.desc()
                )
                .limit(top_k)
            )

            if repository_id is not None:
                statement = statement.where(
                    File.repository_id == repository_id
                )

            results = db.execute(statement).all()

            return [
                (chunk, float(score))
                for chunk, score in results
            ]

        finally:
            db.close()
