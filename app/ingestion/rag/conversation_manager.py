from app.database import SessionLocal
from app.models import Conversation, Message


class ConversationManager:
    def __init__(self):
        self.db = SessionLocal()

    def create_conversation(
        self,
        repository_id: int,
        title: str = "New Conversation",
    ) -> Conversation:
        conversation = Conversation(
            repository_id=repository_id,
            title=title,
        )

        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)

        return conversation

    def get_conversation(
        self,
        conversation_id: int,
    ) -> Conversation | None:
        return (
            self.db.query(Conversation)
            .filter(Conversation.id == conversation_id)
            .first()
        )

    def get_history(
        self,
        conversation_id: int,
    ) -> list[Message]:
        return (
            self.db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at, Message.id)
            .all()
        )

    def save_message(
        self,
        conversation_id: int,
        role: str,
        content: str,
    ) -> Message:
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        return message

    def close(self):
        self.db.close()
