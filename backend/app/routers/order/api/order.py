from core.logger import init_logger
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from app.routers.order.schemas.order import (
    RegisterOrderParams,
    OrderResponse,
    OrderType,
    OrdersPaginateResponse,
)
from core.dependecies.authUser import get_or_make_auth_user
from core.database import User, Order
from core.database.dbHelper import db
import app.routers.order.crud.order as crud
from fastapi_pagination import Params as PaginationParams
from app.routers.order.schemas.order import FilterParams


log = init_logger(__name__)
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
    status_code=status.HTTP_201_CREATED,
)
async def register_order(
    order_params: RegisterOrderParams,
    db_session=Depends(db.get_session),
    user: User = Depends(get_or_make_auth_user),
):

    # https://docs.python.org/3/howto/logging.html#optimization
    if log.isEnabledFor(logging.DEBUG):
        log.debug("register_order params %r for user %s", order_params, user.to_dict())
    order: Order = await crud.create_order(
        db_session=db_session,
        user=user,
        params=order_params,
    )
    if log.isEnabledFor(logging.DEBUG):
        log.debug("order %s", order.to_dict())
    response = OrderResponse(
        order_id=order.id,
        name=order.name,
        weight=order.weight / 1000,
        price=order.price / 100,
        type=order.order_type.name,
        delivery_price=(
            order.delivery_price / 100 if order.delivery_price else "Не расчитано"
        ),
    )
    return response


@router.get(
    "/list/",
)
async def get_order_list(
    pagination_params: PaginationParams = Depends(),
    filter_params: FilterParams = Depends(),
    db_session=Depends(db.get_session),
    user: User = Depends(get_or_make_auth_user),
):
    if log.isEnabledFor(logging.DEBUG):
        log.debug(
            "pagination_params %r filter_params %r for user %r",
            pagination_params,
            filter_params,
            user.to_dict(),
        )
    order_list = dict(
        await crud.get_order_list_paginate(
            db_session=db_session,
            user=user,
            pagination_params=pagination_params,
            filter_params=filter_params,
        )
    )
    prepare_dict = {}
    for k, v in order_list.items():
        if k == "items":
            items = [
                OrderResponse(
                    order_id=item[0],
                    name=item[1],
                    weight=item[2] / 1000,
                    price=item[3] / 100,
                    type=item[4],
                    delivery_price=item[5] / 100 if item[5] else "Не расчитано",
                )
                for item in v
            ]
            prepare_dict[k] = items
            continue
        prepare_dict[k] = order_list[k]

    return OrdersPaginateResponse.model_validate(prepare_dict)


@router.get(
    "/{order_id}/",
    response_model=OrderResponse,
)
async def get_order(
    order_id: int,
    db_session=Depends(db.get_session),
    user: User = Depends(get_or_make_auth_user),
):
    if log.isEnabledFor(logging.DEBUG):
        log.debug("params %r for user %r", order_id, user.to_dict())

    order: Order | None = await crud.get_order(
        db_session=db_session, user=user, order_id=order_id
    )
    if not order:
        log.info("There is no any order for user %r", user.to_dict())
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    response = OrderResponse(
        order_id=order.id,
        name=order.name,
        weight=order.weight / 1000,
        price=order.price / 100,
        type=order.order_type.name,
        delivery_price=(
            order.delivery_price / 100 if order.delivery_price else "Не расчитано"
        ),
    )
    return response
