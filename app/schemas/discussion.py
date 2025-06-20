from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from .user import User
from uuid import UUID

class DiscussionBase(BaseModel):
    title: str
    content: str
    tags: List[str] = []

class DiscussionCreate(DiscussionBase):
    pass

class DiscussionUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None

class DiscussionInDB(DiscussionBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool

class Discussion(DiscussionInDB):
    author: User

class DiscussionWithCommentCount(Discussion):
    comment_count: int

class DiscussionSearchResult(BaseModel):
    id: UUID
    title: str
    content: str
    created_at: datetime
    updated_at: Optional[datetime] = None
  
    comment_count: int
    relevance_score: float
    matched_in: List[str]
    snippet: Optional[str] = None
    
    class Config:
        from_attributes = True

class SearchResponse(BaseModel):
    results: List[DiscussionSearchResult]
    total_count: int
    query: str
    search_time_ms: float