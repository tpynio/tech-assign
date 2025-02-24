from aioresponses import aioresponses
from core.database.redis_helper import redis_storage
from periodic.crud.usd import get_usd_from_redis, saving_usd_to_redis


class TestUsdCrud:

    @classmethod
    async def cleaner(cls):
        redis = await redis_storage.get_pool(redis_storage.DB.CACHES)
        await redis.flushdb()
        return

    async def test_saving_usd_to_redis_get_from_redis_ok(self):
        test_value = 77.777
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        expected_response = {
            "Valute": {
                "USD": {
                    "ID": "R01235",
                    "NumCode": "840",
                    "CharCode": "USD",
                    "Nominal": 1,
                    "Name": "Доллар США",
                    "Value": test_value,
                    "Previous": 90.4268,
                },
            },
        }
        with aioresponses() as mock:
            mock.get(url, payload=expected_response)
            await saving_usd_to_redis()

        value = await get_usd_from_redis()

        assert value == str(test_value)

        await self.cleaner()
