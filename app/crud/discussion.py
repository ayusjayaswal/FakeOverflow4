from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc, or_
from app.models.discussion import Discussion
from app.models.comment import Comment
from app.schemas.discussion import DiscussionCreate, DiscussionUpdate
from typing import List, Optional
from uuid import UUID
import logging

logger = logging.getLogger(__name__)

def get_discussion(db: Session, discussion_id: UUID) -> Optional[Discussion]:
    return db.query(Discussion).options(
        joinedload(Discussion.author)
    ).filter(
        Discussion.id == discussion_id,
        Discussion.is_active == True
    ).first()

def get_discussions(db: Session, skip: int = 0, limit: int = 20, search: Optional[str] = None) -> List[Discussion]:
    query = db.query(Discussion).options(
        joinedload(Discussion.author)
    ).filter(Discussion.is_active == True)
    
    if search and search.strip():
        search_term = search.strip()
        query = query.filter(
            or_(
                Discussion.title.op('%')(search_term),
                Discussion.content.op('%')(search_term),
                Discussion.tags.any(search_term.lower())
            )
        )
    return query.order_by(desc(Discussion.created_at)).offset(skip).limit(limit).all()

def get_discussions_by_user(db: Session, user_id: UUID, skip: int = 0, limit: int = 20) -> List[Discussion]:
    return db.query(Discussion).options(
        joinedload(Discussion.author)
    ).filter(
        Discussion.user_id == user_id,
        Discussion.is_active == True
    ).order_by(desc(Discussion.created_at)).offset(skip).limit(limit).all()

def create_discussion(db: Session, discussion: DiscussionCreate, user_id: UUID) -> Discussion:
    db_discussion = Discussion(
        **discussion.model_dump(),
        user_id=user_id
    )
    db.add(db_discussion)
    db.commit()
    db.refresh(db_discussion)
    return db_discussion

def update_discussion(db: Session, discussion_id: UUID, discussion_update: DiscussionUpdate, user_id: UUID) -> Optional[Discussion]:
    db_discussion = db.query(Discussion).filter(
        Discussion.id == discussion_id,
        Discussion.user_id == user_id,
        Discussion.is_active == True
    ).first()
    
    if not db_discussion:
        return None
    
    update_data = discussion_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_discussion, field, value)
    
    db.commit()
    db.refresh(db_discussion)
    return db_discussion

def delete_discussion(db: Session, discussion_id: UUID, user_id: UUID) -> bool:
    db_discussion = db.query(Discussion).filter(
        Discussion.id == discussion_id,
        Discussion.user_id == user_id,
        Discussion.is_active == True
    ).first()
    
    if not db_discussion:
        return False
    
    db_discussion.is_active = False
    db.commit()
    return True

def get_discussion_comment_count(db: Session, discussion_id: UUID) -> int:
    return db.query(func.count(Comment.id)).filter(
        Comment.discussion_id == discussion_id,
        Comment.is_active == True
    ).scalar()