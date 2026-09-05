from sqlalchemy import Column, BigInteger, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class File(Base):
    __tablename__ = "files"

    id = Column(BigInteger, primary_key=True)

    repository_id = Column(
        BigInteger,
        ForeignKey("repositories.id"),
        nullable=False
    )

    path = Column(Text, nullable=False)
    filename = Column(String(255), nullable=False)
    language = Column(String(100))
    file_size = Column(BigInteger)

    repository = relationship("Repository", back_populates="files")
    chunks = relationship("Chunk", back_populates="file")