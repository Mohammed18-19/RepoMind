from sqlalchemy import Column, BigInteger, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from app.database import Base


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(BigInteger, primary_key=True)

    file_id = Column(
        BigInteger,
        ForeignKey("files.id"),
        nullable=False
    )

    content = Column(Text, nullable=False)
    embedding = Column(Vector(768))
    start_line = Column(Integer, nullable=False)
    end_line = Column(Integer, nullable=False)

    file = relationship("File", back_populates="chunks")