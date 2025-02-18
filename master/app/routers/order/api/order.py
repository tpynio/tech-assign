import logging
from fastapi import APIRouter, Depends, HTTPException, status
from app.routers.order.schemas.order import (
    RegisterOrderParams,
    OrderResponse,
    OrderType,
)
from core.dependecies.authUser import get_or_make_auth_user
from core.database import User, Order
from core.database.dbHelper import db
import app.routers.order.crud.order as crud


log = logging.getLogger(__name__)
router = APIRouter(
    tags=["Orders"],
)


@router.get(
    "/order_types/",
    response_model=list[OrderType],
)
async def get_order_types(db_session=Depends(db.get_session)):
    types = await crud.order_types(db_session=db_session)

    return types


@router.post(
    "/register/",
    response_model=OrderResponse,
)
async def register_order(
    order: RegisterOrderParams,
    db_session=Depends(db.get_session),
    user: User = Depends(get_or_make_auth_user),
):
    order: Order = await crud.create_order(
        db_session=db_session,
        user=user,
        params=order,
    )
    response = OrderResponse(
        order_id=order.id,
        name=order.name,
        weight=order.weight / 1000,
        price=order.price / 100,
        type=order.order_type.name,
    )
    return response


@router.get(
    "/{order_id}/",
    response_model=OrderResponse,
)
async def get_order(
    order_id: int,
    db_session=Depends(db.get_session),
    user: User = Depends(get_or_make_auth_user),
):
    order: Order | None = await crud.get_order(
        db_session=db_session, user=user, order_id=order_id
    )
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    response = OrderResponse(
        order_id=order.id,
        name=order.name,
        weight=order.weight / 1000,
        price=order.price / 100,
        type=order.order_type.name,
    )
    return response
