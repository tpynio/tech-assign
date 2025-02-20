from enum import IntEnum
from typing import Dict

from core.config import settings
from redis.asyncio import Redis
from redis.asyncio.lock import Lock


class RedisDatabase(IntEnum):
    GENERAL = 0
    CACHES = 1
    LOCKS = 2


class RedisHelper:
    DB = RedisDatabase

    def __init__(self, url: str, prefix="redis-cache"):
        self._url = url
        self.decode_responses = True
        self.pools: Dict[int, Redis] = {}
        self._prefix = prefix

    async def get_pool(self, db=DB.CACHES) -> Redis:
        if db not in self.pools:
            redis = Redis.from_url(
                self._url,
                db=int(db),
                encoding="utf-8",
                decode_responses=self.decode_responses,
            )
            self.pools[db] = redis
        return self.pools[db]

    def pool_dependency(self, db=DB.CACHES):
        async def get_pool():
            return await self.get_pool(db)

        return get_pool

    async def get_lock(self, key: str) -> Lock:
        redis = await self.get_pool(db=self.DB.LOCKS)
        return Lock(redis=redis, name=key)


redis_storage = RedisHelper(settings.REDIS_URL)
