from app.routers.binding.crud.binding import binding_free_order
from app.routers.binding.schemas.binding import BindingOrderParams, BindingOrderResponse
from core.database.dbHelper import db
from core.logger import init_logger
from fastapi import APIRouter, Depends

log = init_logger(__name__)
router = APIRouter(
    tags=["OrderBinding"],
)


@router.post(
    "/binding_order/",
    name="try_binding_order",
    response_model=BindingOrderResponse,
    description="Привязка свободных посылок к желающим доставщикам",
)
async def try_binding_order(
    params: BindingOrderParams,
    db_session=Depends(db.get_session),
):
    order = await binding_free_order(db_session, params.delivery_id)
    response = BindingOrderResponse(
        order_id=order.id,
        name=order.name,
        weight=order.weight / 1000,
        price=order.price / 100,
        type=order.order_type.name,
        delivery_price=(
            order.delivery_price / 100 if order.delivery_price else "Не расчитано"
        ),
        delivery_id=order.deliver_id,
    )
    return response
