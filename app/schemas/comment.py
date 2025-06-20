from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from .user import User
from uuid import UUID

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    discussion_id: UUID
    parent_comment_id: Optional[UUID] = None

class CommentUpdate(BaseModel):
    content: Optional[str] = None

class CommentInDB(CommentBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    user_id: UUID
    discussion_id: UUID
    parent_comment_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime
    is_active: bool

class Comment(CommentInDB):
    author: User
    replies: List["Comment"] = []

# For nested comments
Comment.model_rebuild()


