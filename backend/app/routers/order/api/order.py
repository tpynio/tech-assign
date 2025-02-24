import logging

import app.routers.order.crud.order as crud
from app.routers.order.schemas.order import (
    FilterParams,
    OrderResponse,
    OrdersPaginateResponse,
    OrderType,
    RegisterOrderParams,
)
from core.database import Order, User
from core.database.db_helper import db
from core.dependecies.auth_user import get_or_make_auth_user
from core.logger import init_logger
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Params as PaginationParams

log = init_logger(__name__)
router = APIRouter(
    tags=["Orders"],
)


@router.get(
    "/order_types/",
    name="get_order_types",
    description="Получение списка доступных для посылки типов посылок",
    response_model=list[OrderType],
)
async def get_order_types(db_session=Depends(db.get_session)):
    types = await crud.order_types(db_session=db_session)

    return types


@router.post(
    "/register/",
    name="register_order",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    description="Регистрации посылки. При вызове метода, если пользователя нет в системе - он создается",
)
async def register_order(
    order_params: RegisterOrderParams,
    db_session=Depends(db.get_session),
    user: User = Depends(get_or_make_auth_user),
):
    if log.isEnabledFor(logging.DEBUG):
        log.debug("register_order params %r for user %s", order_params, user.to_dict())
    """
    https://docs.python.org/3/howto/logging.html#optimization
    - to_dict - достаточно жирная операция, чтобы избежать расходов при форматировании параметров лога
    по рекомендации от logging по оптимизации добавлена проверка на соответствие уровню логирования
    """

    order: Order | None = await crud.create_order(
        db_session=db_session,
        user=user,
        params=order_params,
    )
    if not Order:
        log.info("Can't create order")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

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
    name="get_order_list",
    response_model=OrdersPaginateResponse,
    description="Получение списка посылок пользователя."
    " При вызове метода, если пользователя нет в системе - он создается",
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
    name="get_order",
    response_model=OrderResponse,
    description="Получение посылки пользователя. При вызове метода, если пользователя нет в системе - он создается",
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
