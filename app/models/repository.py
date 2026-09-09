from sqlalchemy import Column, BigInteger, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.database import Base


class Repository(Base):
    __tablename__ = "repositories"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(255), nullable=False)
    repo_metadata = Column(JSONB)
    file_count = Column(Integer, nullable=False, default=0)

    files = relationship("File", back_populates="repository")
    conversations = relationship(
        "Conversation",
        back_populates="repository"
    )