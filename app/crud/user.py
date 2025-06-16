from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.user import User
from app.models.discussion import Discussion
from app.models.comment import Comment
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from typing import Optional

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id, User.is_active == True).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username, User.is_active == True).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email, User.is_active == True).first()

def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

def get_user_stats(db: Session, user_id: int) -> dict:
    discussion_count = db.query(func.count(Discussion.id)).filter(
        Discussion.user_id == user_id, Discussion.is_active == True
    ).scalar()
    
    comment_count = db.query(func.count(Comment.id)).filter(
        Comment.user_id == user_id, Comment.is_active == True
    ).scalar()
    
    return {
        "discussion_count": discussion_count,
        "comment_count": comment_count
    }
