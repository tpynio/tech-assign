import logging
from fastapi import APIRouter, Depends
from app.routers.order.schemas.order import (
    RegisterOrderParams,
    RegisterOrderResponse,
    OrderType,
)
from core.dependecies.authUser import get_or_make_auth_user
from core.database import User, Order
from core.database.dbHelper import db
from app.routers.order.crud.order import create_order, order_types


log = logging.getLogger(__name__)
router = APIRouter(
    tags=["Orders"],
)


@router.get(
    "/order_types/",
    response_model=list[OrderType],
)
async def get_order_types(db_session=Depends(db.get_session)):
    types = await order_types(db_session=db_session)

    return types


@router.post(
    "/register/",
    response_model=RegisterOrderResponse,
)
async def register_order(
    order: RegisterOrderParams,
    db_session=Depends(db.get_session),
    user: User = Depends(get_or_make_auth_user),
):
    order: Order = await create_order(
        db_session=db_session,
        user=user,
        params=order,
    )
    response = RegisterOrderResponse(order_id=order.id)
    return response
