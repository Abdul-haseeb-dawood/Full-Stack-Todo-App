from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.message_repository import ConversationRepository, MessageRepository
from app.schemas.message import ConversationCreate, MessageCreate
import uuid


class ConversationService:
    def __init__(self, db_session: AsyncSession):
        self.conversation_repo = ConversationRepository(db_session)

    async def create_conversation(self, conversation_data: ConversationCreate) -> ConversationCreate:
        return await self.conversation_repo.create_conversation(conversation_data)

    async def get_conversation_by_id(self, conversation_id: uuid.UUID) -> Optional[ConversationCreate]:
        return await self.conversation_repo.get_conversation_by_id(conversation_id)

    async def get_conversations_by_user(self, user_id: str) -> List[ConversationCreate]:
        return await self.conversation_repo.get_conversations_by_user(user_id)

    async def update_conversation(self, conversation_id: uuid.UUID, conversation_data: ConversationCreate) -> Optional[ConversationCreate]:
        return await self.conversation_repo.update_conversation(conversation_id, conversation_data)

    async def delete_conversation(self, conversation_id: uuid.UUID) -> bool:
        return await self.conversation_repo.delete_conversation(conversation_id)


class MessageService:
    def __init__(self, db_session: AsyncSession):
        self.message_repo = MessageRepository(db_session)

    async def create_message(self, message_data: MessageCreate) -> MessageCreate:
        return await self.message_repo.create_message(message_data)

    async def get_messages_by_conversation(self, conversation_id: uuid.UUID) -> List[MessageCreate]:
        return await self.message_repo.get_messages_by_conversation(conversation_id)

    async def get_message_by_id(self, message_id: uuid.UUID) -> Optional[MessageCreate]:
        return await self.message_repo.get_message_by_id(message_id)

    async def get_messages_by_user(self, user_id: str) -> List[MessageCreate]:
        return await self.message_repo.get_messages_by_user(user_id)

    async def update_message(self, message_id: uuid.UUID, content: str) -> Optional[MessageCreate]:
        return await self.message_repo.update_message(message_id, content)

    async def delete_message(self, message_id: uuid.UUID) -> bool:
        return await self.message_repo.delete_message(message_id)