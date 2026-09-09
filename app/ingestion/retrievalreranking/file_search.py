import re

from sqlalchemy import select

from app.database import SessionLocal
from app.models.file import File


class FileSearch:

    FILE_PATTERNS = [
        r"\bfile\s+named\s+[`'\"]?([^`'\"\s?]+)",
        r"\bfile\s+called\s+[`'\"]?([^`'\"\s?]+)",
    ]

    def extract_filename(
        self,
        query: str,
    ) -> str | None:

        for pattern in self.FILE_PATTERNS:

            match = re.search(
                pattern,
                query,
                re.IGNORECASE,
            )

            if match:
                return match.group(1).rstrip(
                    ".,!?"
                )

        return None

    def exists(
        self,
        query: str,
        repository_id: int,
    ) -> bool | None:

        filename = self.extract_filename(query)

        if filename is None:
            return None

        db = SessionLocal()

        try:

            statement = (
                select(File.id)
                .where(
                    File.repository_id
                    == repository_id
                )
                .where(
                    (File.filename == filename)
                    | (File.path == filename)
                )
                .limit(1)
            )

            result = db.execute(
                statement
            ).first()

            return result is not None

        finally:
            db.close()
