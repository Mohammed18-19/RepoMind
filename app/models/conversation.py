from datetime import datetime

from sqlalchemy import Column, BigInteger, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(BigInteger, primary_key=True)

    repository_id = Column(
        BigInteger,
        ForeignKey("repositories.id"),
        nullable=False
    )

    title = Column(String(255))

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    repository = relationship(
        "Repository",
        back_populates="conversations"
    )

    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="Message.created_at"
    )