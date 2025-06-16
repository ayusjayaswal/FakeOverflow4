from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_active_user
from app.crud.user import get_user, get_user_stats
from app.schemas.user import User, UserWithStats
from app.utils.cache import Cache, get_user_cache_key
from typing import List

router = APIRouter()

@router.get("/me", response_model=UserWithStats)
def read_users_me(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    cache_key = get_user_cache_key(current_user.id)
    cached_user = Cache.get(cache_key)
    if cached_user:
        return cached_user
    
    stats = get_user_stats(db, current_user.id)
    user_with_stats = UserWithStats(
        **current_user.__dict__,
        **stats
    )
    Cache.set(cache_key, user_with_stats, 300)
    return user_with_stats


@router.get("/{user_id}", response_model=UserWithStats)
def read_user(user_id: int, db: Session = Depends(get_db)):
    cache_key = get_user_cache_key(user_id)
    cached_user = Cache.get(cache_key)
    if cached_user:
        return cached_user
    
    user = get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    stats = get_user_stats(db, user_id)
    user_with_stats = UserWithStats(
        **user.__dict__,
        **stats
    )
    
    Cache.set(cache_key, user_with_stats, 300)
    return user_with_stats