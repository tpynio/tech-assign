from core.logger import init_logger
from fastapi import APIRouter, HTTPException, status
from periodic.crud.usd import saving_usd_to_redis, get_usd_from_redis
from periodic.crud.orderCalculate import order_delivery_calculate
from app.routers.periodic.schemas.periodic import (
    CachedUSDData,
    ForceRecalculate,
    CachedUSDValue,
)


log = init_logger(__name__)
router = APIRouter(
    tags=["Periodic"],
)


@router.post(
    "/force_cache_usd_data/",
    response_model=CachedUSDData,
)
async def force_cache_usd_data():
    usd_data = await saving_usd_to_redis()
    if not usd_data:
        log.error("Can't get usd-data")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return usd_data


@router.get(
    "/get_cached_usd_data/",
    response_model=CachedUSDValue,
)
async def get_cached_usd_data():
    usd_value = await get_usd_from_redis()

    return {"value": usd_value}


@router.post(
    "/force_delivery_recalculate/",
    response_model=ForceRecalculate,
)
async def force_delivery_recalculate():
    await order_delivery_calculate()

    return {"status": "success"}
