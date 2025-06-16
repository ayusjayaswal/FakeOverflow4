import redis
import json
import pickle
from typing import Any, Optional
from app.core.config import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=False)

class Cache:
    @staticmethod
    def set(key: str, value: Any, expire: Optional[int] = None) -> bool:
        try:
            if expire is None:
                expire = settings.CACHE_EXPIRE_SECONDS
            
            serialized_value = pickle.dumps(value)
            return redis_client.setex(key, expire, serialized_value)
        except Exception as e:
            print(f"Cache set error: {e}")
            return False

    @staticmethod
    def get(key: str) -> Any:
        try:
            value = redis_client.get(key)
            if value is None:
                return None
            return pickle.loads(value)
        except Exception as e:
            print(f"Cache get error: {e}")
            return None

    @staticmethod
    def delete(key: str) -> bool:
        try:
            return bool(redis_client.delete(key))
        except Exception as e:
            print(f"Cache delete error: {e}")
            return False

    @staticmethod
    def delete_pattern(pattern: str) -> int:
        try:
            keys = redis_client.keys(pattern)
            if keys:
                return redis_client.delete(*keys)
            return 0
        except Exception as e:
            print(f"Cache delete pattern error: {e}")
            return 0

    @staticmethod
    def exists(key: str) -> bool:
        try:
            return bool(redis_client.exists(key))
        except Exception as e:
            print(f"Cache exists error: {e}")
            return False


# Cache key generators
def get_discussions_cache_key(skip: int, limit: int, search: Optional[str] = None) -> str:
    search_part = f"_search_{search}" if search else ""
    return f"discussions_{skip}_{limit}{search_part}"


def get_discussion_cache_key(discussion_id: int) -> str:
    return f"discussion_{discussion_id}"


def get_comments_cache_key(discussion_id: int) -> str:
    return f"comments_discussion_{discussion_id}"


def get_user_cache_key(user_id: int) -> str:
    return f"user_{user_id}"


# Cache invalidation helpers
def invalidate_discussion_cache(discussion_id: int):
    Cache.delete(get_discussion_cache_key(discussion_id))
    Cache.delete(get_comments_cache_key(discussion_id))
    Cache.delete_pattern("discussions_*")


def invalidate_user_cache(user_id: int):
    Cache.delete(get_user_cache_key(user_id))


def invalidate_comments_cache(discussion_id: int):
    Cache.delete(get_comments_cache_key(discussion_id))
