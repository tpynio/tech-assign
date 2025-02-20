from typing import Dict

import aiohttp
from core.config import settings
from core.database.redisHelper import redis_storage
from core.logger import init_logger

log = init_logger(__name__)


lock_key = f"{settings.REDIS_LOCK_PREFIX}-dollar"
redis_record_key = f"{settings.REDIS_KEY_PREFIX}-dollar"


async def get_usd_info():
    url = "https://www.cbr-xml-daily.ru/daily_json.js"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data: Dict = await response.json(content_type=None)
                usd_info = data["Valute"]["USD"]
                log.info("USD data is %r", usd_info)
                return usd_info
    except Exception as exc:
        log.error("Can't connect to cbr-xml-daily", exc_info=exc)
        return None


async def save_to_redis(value: str):
    expire_in = settings.REDIS_EXPIRE

    redis = await redis_storage.get_pool(redis_storage.DB.CACHES)
    lock = await redis_storage.get_lock(lock_key)
    async with lock:
        await redis.set(redis_record_key, value, ex=expire_in)


async def saving_usd_to_redis():
    usd_info: Dict | None = await get_usd_info()
    if usd_info:
        value = usd_info.get("Value")
        await save_to_redis(value)

    return usd_info


async def get_usd_from_redis():
    redis = await redis_storage.get_pool(redis_storage.DB.CACHES)
    lock = await redis_storage.get_lock(lock_key)
    async with lock:
        value = await redis.get(redis_record_key)
    return value
