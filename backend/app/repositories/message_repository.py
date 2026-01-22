from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, desc
from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.message import ConversationCreate, MessageCreate
import uuid


class ConversationRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_conversation(self, conversation_data: ConversationCreate) -> Conversation:
        conversation = Conversation(**conversation_data.model_dump())
        self.db_session.add(conversation)
        await self.db_session.commit()
        await self.db_session.refresh(conversation)
        return conversation

    async def get_conversation_by_id(self, conversation_id: uuid.UUID) -> Optional[Conversation]:
        result = await self.db_session.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        return result.scalar_one_or_none()

    async def get_conversations_by_user(self, user_id: str) -> List[Conversation]:
        result = await self.db_session.execute(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(desc(Conversation.created_at))
        )
        return result.scalars().all()

    async def update_conversation(self, conversation_id: uuid.UUID, conversation_data: ConversationCreate) -> Optional[Conversation]:
        conversation = await self.get_conversation_by_id(conversation_id)
        if conversation:
            for key, value in conversation_data.model_dump().items():
                setattr(conversation, key, value)
            await self.db_session.commit()
            await self.db_session.refresh(conversation)
        return conversation

    async def delete_conversation(self, conversation_id: uuid.UUID) -> bool:
        conversation = await self.get_conversation_by_id(conversation_id)
        if conversation:
            await self.db_session.delete(conversation)
            await self.db_session.commit()
            return True
        return False


class MessageRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_message(self, message_data: MessageCreate) -> Message:
        message = Message(**message_data.model_dump())
        self.db_session.add(message)
        await self.db_session.commit()
        await self.db_session.refresh(message)
        return message

    async def get_messages_by_conversation(self, conversation_id: uuid.UUID) -> List[Message]:
        result = await self.db_session.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
        )
        return result.scalars().all()

    async def get_message_by_id(self, message_id: uuid.UUID) -> Optional[Message]:
        result = await self.db_session.execute(
            select(Message).where(Message.id == message_id)
        )
        return result.scalar_one_or_none()

    async def get_messages_by_user(self, user_id: str) -> List[Message]:
        result = await self.db_session.execute(
            select(Message)
            .where(Message.user_id == user_id)
            .order_by(Message.created_at.desc())
        )
        return result.scalars().all()

    async def update_message(self, message_id: uuid.UUID, content: str) -> Optional[Message]:
        message = await self.get_message_by_id(message_id)
        if message:
            message.content = content
            await self.db_session.commit()
            await self.db_session.refresh(message)
        return message

    async def delete_message(self, message_id: uuid.UUID) -> bool:
        message = await self.get_message_by_id(message_id)
        if message:
            await self.db_session.delete(message)
            await self.db_session.commit()
            return True
        return False