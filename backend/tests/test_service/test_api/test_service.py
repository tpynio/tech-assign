from app.main_router import main_router as app
from app.routers.service.schemas.service import PingResponse
from fastapi import status


def test_sync_ping(client):
    ping_url = app.url_path_for("ping")
    response = client.get(ping_url)
    assert response.status_code == 200
    result_json = response.json()
    assert PingResponse(**result_json).message == "pong"


async def test_ping(
    async_client,
):
    ping_url = app.url_path_for("ping")

    response = await async_client.get(
        url=ping_url,
    )

    assert response.status_code == status.HTTP_200_OK, response.text
    result_json = response.json()

    assert PingResponse(**result_json).message == "pong"
