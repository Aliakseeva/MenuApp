import json
from typing import Any

from .database import redis_client


class Cache:
    @staticmethod
    def get_from_cache(route: str) -> dict | list[dict] | None:
        """Get value from cache with 'route' as a key if exists, else -- None"""
        val = redis_client.get(route)
        if val:
            return json.loads(val)
        return val

    @staticmethod
    def set_to_cache(route: str, val: Any) -> None:
        """Set value to cache with 'route' as a key"""
        redis_client.set(route, json.dumps(val))

    @staticmethod
    def clear_cache(route: str) -> None:
        """Clear value with 'route' as a key in cache"""
        keys = redis_client.keys(f'{route}*')
        if keys:
            redis_client.delete(*keys)
