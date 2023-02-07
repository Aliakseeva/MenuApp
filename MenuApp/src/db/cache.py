import aioredis
from MenuApp.src.db.config import settings


redis_client = aioredis.from_url(
    url=settings.CACHE_REDIS_URL, db=settings.REDIS_DB, decode_responses=True)
