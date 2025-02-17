import logging
from fastapi import (
    APIRouter,
)
from app.routers.order.schemas.order import RegisterOrderParams, RegisterOrderResponse


log = logging.getLogger(__name__)
router = APIRouter(
    tags=["Orders"],
)


@router.post(
    "/register",
    response_model=RegisterOrderResponse,
)
async def register_order(
    order: RegisterOrderParams,
):
    response = RegisterOrderResponse(order_id=777)
    return response
