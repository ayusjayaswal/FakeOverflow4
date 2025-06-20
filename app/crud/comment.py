from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate
from typing import List, Optional
from uuid import UUID

def get_comment(db: Session, comment_id: UUID) -> Optional[Comment]:
    return db.query(Comment).options(
        joinedload(Comment.author)
    ).filter(
        Comment.id == comment_id,
        Comment.is_active == True
    ).first()

def get_comments_by_discussion(db: Session, discussion_id: UUID, skip: int = 0, limit: int = 50) -> List[Comment]:
    return db.query(Comment).options(
        joinedload(Comment.author)
    ).filter(
        Comment.discussion_id == discussion_id,
        Comment.is_active == True
    ).order_by(Comment.created_at).offset(skip).limit(limit).all()

def get_comments_tree(db: Session, discussion_id: UUID) -> List[Comment]:
    return (
        db.query(Comment)
        .options(
            joinedload(Comment.author),
            joinedload(Comment.replies).joinedload(Comment.replies)
        )
        .filter(
            Comment.discussion_id == discussion_id,
            Comment.is_active == True,
            Comment.parent_comment_id == None
        )
        .order_by(Comment.created_at)
        .all()
    )

def create_comment(db: Session, comment: CommentCreate, user_id: UUID) -> Comment:
    db_comment = Comment(
        **comment.model_dump(),
        user_id=user_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def update_comment(db: Session, comment_id: UUID, comment_update: CommentUpdate, user_id: UUID) -> Optional[Comment]:
    db_comment = db.query(Comment).filter(
        Comment.id == comment_id,
        Comment.user_id == user_id,
        Comment.is_active == True
    ).first()
    if not db_comment:
        return None
    update_data = comment_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_comment, field, value)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def delete_comment(db: Session, comment_id: UUID, user_id: UUID) -> bool:
    db_comment = db.query(Comment).filter(
        Comment.id == comment_id,
        Comment.user_id == user_id,
        Comment.is_active == True
    ).first()
    if not db_comment:
        return False
    
    db_comment.is_active = False
    db.commit()
    return True
