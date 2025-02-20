import asyncio

from app.mainRouter import main_router as app
from app.routers.binding.schemas.binding import BindingOrderParams, BindingOrderResponse
from fastapi import status


class TestOrderBinding:

    async def test_order_binding_first_is_first_ok(
        self,
        async_client,
        async_session,
        order_dummies_factory,
    ):
        # Два доставщика
        delivery_id_0 = 777
        delivery_id_1 = 666

        # Одна посылка
        order_fields = {
            "name": "test_get_order_ok",
            "weight": 5000,
            "order_type": "Misc",
            "price": 11599,
            "delivery_price": None,
            "delivery_id": None,
        }
        await order_dummies_factory.make_dummies(**order_fields)

        url = app.url_path_for(
            "try_binding_order",
        )

        response0 = async_client.post(
            url=url,
            json=BindingOrderParams(delivery_id=delivery_id_0).model_dump(),
        )
        response1 = async_client.post(
            url=url,
            json=BindingOrderParams(delivery_id=delivery_id_1).model_dump(),
        )
        tasks = [response0, response1]
        responses = await asyncio.gather(*tasks)

        # первый получает заказ
        assert responses[0].status_code == status.HTTP_200_OK
        json_response = responses[0].json()
        parse_answer = BindingOrderResponse(**json_response)
        assert parse_answer.delivery_id == delivery_id_0

        assert responses[1].status_code == status.HTTP_404_NOT_FOUND
        json_response = responses[1].json()
        assert json_response["detail"] == "There are no any free orders"
