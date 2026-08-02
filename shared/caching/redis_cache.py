from typing import Optional
from shared.config import REDIS_URL
from shared.logger import logger

class RedisCache:
    """
    Redis caching service wrapper with optional graceful fallback.
    """

    def __init__(self, redis_url: str = REDIS_URL):
        self.redis_url = redis_url
        self.client = None
        try:
            import redis
            self.client = redis.from_url(redis_url)
        except Exception as e:
            logger.warning(f"Redis cache client initialization failed: {e}")

    def get(self, key: str) -> Optional[str]:
        if not self.client:
            return None
        try:
            val = self.client.get(key)
            return val.decode("utf-8") if val else None
        except Exception as e:
            logger.warning(f"Redis get error for key '{key}': {e}")
            return None

    def set(self, key: str, value: str, ex: Optional[int] = 3600):
        if not self.client:
            return
        try:
            self.client.set(key, value, ex=ex)
        except Exception as e:
            logger.warning(f"Redis set error for key '{key}': {e}")
