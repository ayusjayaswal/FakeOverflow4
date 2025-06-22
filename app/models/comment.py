import uuid
from sqlalchemy import Column, Integer, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(Text, nullable=False)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    discussion_id = Column(UUID, ForeignKey("discussions.id"), nullable=False)
    parent_comment_id = Column(UUID, ForeignKey("comments.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)

    # Relationships
    author = relationship("User", back_populates="comments")
    discussion = relationship("Discussion", back_populates="comments")
    parent = relationship("Comment", remote_side=[id], backref="replies")
