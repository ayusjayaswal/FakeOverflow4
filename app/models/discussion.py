import uuid
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, ARRAY
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class Discussion(Base):
    __tablename__ = "discussions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(ARRAY(String), default=[])
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)

    # Relationships
    author = relationship("User", back_populates="discussions")
    comments = relationship("Comment", back_populates="discussion", cascade="all, delete-orphan")

