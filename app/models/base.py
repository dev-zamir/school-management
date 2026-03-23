from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db.session import Base


class TimestampMixin:
    """Adds created_at and updated_at to any model — like Rails' timestamps"""
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class UUIDMixin:
    """Use UUID as primary key instead of integer"""
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
