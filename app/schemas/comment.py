from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from .user import User

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    discussion_id: int
    parent_comment_id: Optional[int] = None

class CommentUpdate(BaseModel):
    content: Optional[str] = None

class CommentInDB(CommentBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    discussion_id: int
    parent_comment_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    is_active: bool

class Comment(CommentInDB):
    author: User
    replies: List["Comment"] = []

# For nested comments
Comment.model_rebuild()


