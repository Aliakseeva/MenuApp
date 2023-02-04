import json
from typing import Any

from .database import redis_client


class Cache:
    @staticmethod
    async def get_from_cache(route: str) -> dict | list[dict] | None:
        """Get value from cache with 'route' as a key if exists, else -- None"""
        val = await redis_client.get(route)
        if val:
            return json.loads(val)
        return val

    @staticmethod
    async def set_to_cache(route: str, val: Any) -> None:
        """Set value to cache with 'route' as a key"""
        await redis_client.set(route, json.dumps(val), ex=300)

    @staticmethod
    async def clear_cache(route: str) -> None:
        """Clear value with 'route' as a key in cache"""
        keys = await redis_client.keys(f"{route}*")
        if keys:
            await redis_client.delete(*keys)
