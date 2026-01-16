from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declared_attr
from app.db.database import Base


class TimestampMixin:
    """Mixin class to add created_at and updated_at timestamps to models"""

    @declared_attr
    def created_at(cls):
        return Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    @declared_attr
    def updated_at(cls):
        return Column(DateTime(timezone=True), server_default=func.now(),
                     onupdate=func.now(), nullable=False)


class BaseModel(Base):
    """Base model class with common functionality"""
    __abstract__ = True

    # Include the timestamp mixin
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),
                       onupdate=func.now(), nullable=False)


# Import all models here to ensure they are registered with SQLAlchemy
# Note: Avoid importing here to prevent circular imports; instead, import in the main app