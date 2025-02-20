from app.mainRouter import main_router as app
from fastapi import status
from core.config import settings
from core.database.models.user import User
from core.database.models.order import Order, OrderTypes
from app.routers.order.schemas.order import OrderResponse
import uuid


# @mock.patch("app.routers.order.crud.order.order_types", autospec=True)
async def test_get_order_types(
    # mock_order_types,
    async_client,
    async_session,
):
    url = app.url_path_for("get_order_types")
    response = await async_client.get(
        url=url,
    )

    assert response.status_code == status.HTTP_200_OK, response.text
    result_json = response.json()

    assert result_json[0]["name"] == OrderTypes[0]
    assert result_json[1]["name"] == OrderTypes[1]
    assert result_json[2]["name"] == OrderTypes[2]


class TestRegisterOrder:

    async def test_register_order_ok(
        self,
        async_client,
        async_session,
        auth_user: User,
        auth_user_session_id,
    ):
        test_value = {
            "name": "test",
            "weight": 15,
            "type": "Misc",
            "price": 115.99,
        }
        url = app.url_path_for("register_order")
        session_id = uuid.UUID(bytes=auth_user.id).hex
        response = await async_client.post(
            url=url,
            json=test_value,
            cookies={settings.COOKIE_SESSION_ID_KEY_NAME: str(session_id)},
        )

        assert response.status_code == status.HTTP_201_CREATED, response.text
        parsed_resp = OrderResponse(**response.json())

        assert parsed_resp.name == test_value["name"]
        assert parsed_resp.type == test_value["type"]
        assert parsed_resp.weight == test_value["weight"]
        assert parsed_resp.price == test_value["price"]
        assert parsed_resp.delivery_price == "Не расчитано"

        order_id = parsed_resp.order_id
        order = await async_session.get(Order, order_id)

        assert order is not None
        await async_session.delete(order)
        await async_session.commit()

    async def test_register_order_non_validated(
        self,
        async_client,
        async_session,
        auth_user: User,
        auth_user_session_id,
    ):
        test_value = {
            "name": "test",
            "weight": -15,
            "type": "UNKNOWN_TYPE",
            "price": -115.99,
        }
        url = app.url_path_for("register_order")
        session_id = uuid.UUID(bytes=auth_user.id).hex
        response = await async_client.post(
            url=url,
            json=test_value,
            cookies={settings.COOKIE_SESSION_ID_KEY_NAME: str(session_id)},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        json_response = response.json()
        possible_errors = (
            "Value error, weight must be greater or equal than 0",
            "Input should be 'Clothes', 'Electronics' or 'Misc'",
            "Value error, price_value must be greater or equal than 0",
        )
        errors = json_response["detail"]
        for err in errors:
            assert err["msg"] in possible_errors
