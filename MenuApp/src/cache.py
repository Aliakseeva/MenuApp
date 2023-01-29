import json

from .database import redis_client


class Cache:
    @staticmethod
    def get_from_cache(route):
        val = redis_client.get(route)
        if val:
            return json.loads(val)
        return val

    @staticmethod
    def set_to_cache(route, val):
        redis_client.set(route, json.dumps(val))

    @staticmethod
    def clear_cache(route):
        keys = redis_client.keys(f'{route}*')
        if keys:
            redis_client.delete(*keys)
