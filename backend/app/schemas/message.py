from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class ConversationBase(BaseModel):
    user_id: str


class ConversationCreate(ConversationBase):
    pass


class ConversationUpdate(ConversationBase):
    pass


class Conversation(ConversationBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MessageBase(BaseModel):
    user_id: str
    conversation_id: uuid.UUID
    role: str  # 'user' or 'assistant'
    content: str


class MessageCreate(MessageBase):
    pass


class MessageUpdate(BaseModel):
    content: Optional[str] = None


class Message(MessageBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True