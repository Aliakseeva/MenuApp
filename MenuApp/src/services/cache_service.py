import json
from dataclasses import dataclass
from typing import Any, AsyncGenerator
from fastapi.encoders import jsonable_encoder


@dataclass
class CacheService:
    cache: AsyncGenerator

    async def get(self, route: str) -> dict | list[dict] | None:
        """Get value from cache with 'route' as a key if exists, else -- None"""
        val = await self.cache.get(route)
        if val:
            return json.loads(val)
        return val

    async def set(self, route: str, val: Any) -> None:
        """Set value to cache with 'route' as a key"""
        val = jsonable_encoder(val)
        return await self.cache.set(route, json.dumps(val))

    async def clear(self) -> None:
        """Clear value with 'route' as a key in cache"""
        return await self.cache.flushdb()
