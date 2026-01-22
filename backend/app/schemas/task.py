from pydantic import BaseModel, Field
from pydantic.config import ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime


class TaskBase(BaseModel):
    user_id: Optional[str] = None
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    completed: bool = False
    priority: str = Field(default='medium', min_length=1, max_length=20)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    user_id: Optional[str] = None
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None
    priority: Optional[str] = Field(None, min_length=1, max_length=20)


class TaskResponse(TaskBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)