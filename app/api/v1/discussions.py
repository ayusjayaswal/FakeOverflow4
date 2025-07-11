from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_active_user
from app.crud.discussion import (
    get_discussion, get_discussions, get_discussions_by_user,
    create_discussion, update_discussion, delete_discussion,
    get_discussion_comment_count
)
from app.schemas.discussion import Discussion, DiscussionCreate, DiscussionUpdate, DiscussionWithCommentCount
from app.models.user import User
from app.utils.cache import (
    Cache, get_discussions_cache_key, get_discussion_cache_key,
    invalidate_discussion_cache
)
from typing import List, Optional
from uuid import UUID

router = APIRouter()
        
@router.get("/", response_model=List[DiscussionWithCommentCount])
def read_discussions(
    skip: int = 0,
    limit: int = Query(default=20, le=100),
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    cache_key = get_discussions_cache_key(skip, limit, search)
    cached_discussions = Cache.get(cache_key)
    if cached_discussions:
        return cached_discussions
    discussions = get_discussions(db, skip, limit, search)
    discussions_with_counts = []
    for discussion in discussions:
        comment_count = get_discussion_comment_count(db, discussion.id)
        discussion_with_count = DiscussionWithCommentCount(
            **discussion.__dict__,
            comment_count=comment_count
        )
        discussions_with_counts.append(discussion_with_count)
    Cache.set(cache_key, discussions_with_counts, 300)
    return discussions_with_counts

@router.post("/", response_model=Discussion)
def create_new_discussion(
    discussion: DiscussionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_discussion = create_discussion(db, discussion, current_user.id)
    Cache.delete_pattern("discussions_*")
    return db_discussion

@router.get("/{discussion_id}", response_model=Discussion)
def read_discussion(discussion_id: UUID, db: Session = Depends(get_db)):
    cache_key = get_discussion_cache_key(discussion_id)
    cached_discussion = Cache.get(cache_key)
    if cached_discussion:
        return cached_discussion
    
    discussion = get_discussion(db, discussion_id)
    if discussion is None:
        raise HTTPException(status_code=404, detail="Discussion not found")
    
    Cache.set(cache_key, discussion, 300)
    return discussion

@router.put("/{discussion_id}", response_model=Discussion)
def update_existing_discussion(
    discussion_id: UUID,
    discussion_update: DiscussionUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    discussion = update_discussion( db, discussion_id, discussion_update, current_user.id)
    if discussion is None:
        raise HTTPException(status_code=404, detail="Discussion not found or not owned by user")
    
    invalidate_discussion_cache(discussion_id)
    return discussion

@router.delete("/{discussion_id}")
def delete_existing_discussion(
    discussion_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    success = delete_discussion(db, discussion_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Discussion not found or not owned by user")
    
    invalidate_discussion_cache(discussion_id)
    return {"message": "Discussion deleted successfully"}

@router.get("/user/{user_id}", response_model=List[Discussion])
def read_user_discussions(
    user_id: UUID,
    skip: int = 0,
    limit: int = Query(default=20, le=100),
    db: Session = Depends(get_db)
):
    return get_discussions_by_user(db, user_id, skip, limit)