from sqlalchemy import Column, String, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import BaseModel
import uuid


class Task(BaseModel):
    __tablename__ = "tasks"

    # Using PostgreSQL UUID type
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(255), nullable=False, index=True)  # String to accommodate various user ID formats
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, nullable=False, default=False)
    priority = Column(String(20), nullable=False, default='medium')