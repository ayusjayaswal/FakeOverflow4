from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_active_user
from app.crud.comment import (
    get_comment, get_comments_by_discussion, get_comments_tree,
    create_comment, update_comment, delete_comment
)
from app.schemas.comment import Comment, CommentCreate, CommentUpdate
from app.models.user import User
from app.utils.cache import Cache, get_comments_cache_key, invalidate_comments_cache
from typing import List
from uuid import UUID
from pydantic import parse_obj_as

router = APIRouter()

@router.get("/discussion/{discussion_id}", response_model=List[Comment])
def read_discussion_comments(
    discussion_id: UUID,
    tree: bool = Query(default=True, description="Return comments in tree structure"),
    skip: int = 0,
    limit: int = Query(default=50, le=200),
    db: Session = Depends(get_db)
):
    if tree:
        cache_key = get_comments_cache_key(discussion_id)
        cached_comments = Cache.get(cache_key)
        if cached_comments:
            return cached_comments
        
        comments = get_comments_tree(db, discussion_id=discussion_id)
        pydantic_comments = parse_obj_as(List[Comment], comments)
        Cache.set(cache_key, comments, 300)
        return pydantic_comments
    else:
        return get_comments_by_discussion(db, discussion_id=discussion_id, skip=skip, limit=limit)

@router.post("/", response_model=Comment)
def create_new_comment(
    comment: CommentCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_comment = create_comment(db=db, comment=comment, user_id=current_user.id)
    
    invalidate_comments_cache(comment.discussion_id)
    
    return db_comment

@router.get("/{comment_id}", response_model=Comment)
def read_comment(comment_id: UUID, db: Session = Depends(get_db)):
    comment = get_comment(db, comment_id=comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

@router.put("/{comment_id}", response_model=Comment)
def update_existing_comment(
    comment_id: UUID,
    comment_update: CommentUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    comment = update_comment(
        db=db,
        comment_id=comment_id,
        comment_update=comment_update,
        user_id=current_user.id
    )
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found or not owned by user")
    invalidate_comments_cache(comment.discussion_id)
    return comment

@router.delete("/{comment_id}")
def delete_existing_comment(
    comment_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    comment = get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    success = delete_comment(db=db, comment_id=comment_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found or not owned by user")
    invalidate_comments_cache(comment.discussion_id)
    return {"message": "Comment deleted successfully"}
