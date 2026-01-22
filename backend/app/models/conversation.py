from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import BaseModel
import uuid


class Conversation(BaseModel):
    __tablename__ = "conversations"

    # Using PostgreSQL UUID type
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(255), nullable=False, index=True)  # String to accommodate various user ID formats