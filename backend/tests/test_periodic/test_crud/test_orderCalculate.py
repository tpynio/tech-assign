from core.database.models.order import Order
from core.database.redisHelper import redis_storage
from periodic.crud.orderCalculate import order_delivery_calculate
from periodic.crud.usd import redis_record_key


class TestOrderCalculate:

    async def test_order_calculate_ok(
        self,
        async_session,
        auth_user,
        order_dummies_factory,
    ):
        dollar_value = 77.777
        redis = await redis_storage.get_pool(redis_storage.DB.CACHES)
        await redis.set(redis_record_key, str(dollar_value), ex=30)

        order_fields = {
            "name": "test_get_order_list_ok",
            "weight": 5000,
            "order_type": "Misc",
            "price": 11599,
            "delivery_price": None,
        }
        # Стоимость = (вес в кг * 0.5 + стоимость содержимого в долларах * 0.01 ) * курс доллара к рублю
        calculated_value = int((5 * 0.5 + 115.99 * 0.01) * 77.777 * 100)  # 28465 коп.

        order: Order = await order_dummies_factory.make_dummies(**order_fields)
        print(f"test calculated_value = {calculated_value}")

        await order_delivery_calculate()

        await async_session.refresh(order)

        assert order.delivery_price == calculated_value
