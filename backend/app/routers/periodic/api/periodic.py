from core.logger import init_logger
from fastapi import APIRouter, HTTPException, status
from periodic.crud.usd import saving_usd_to_redis, get_usd_from_redis
from app.routers.periodic.schemas.periodic import CacheUsdData


log = init_logger(__name__)
router = APIRouter(
    tags=["Periodic"],
)


@router.post(
    "/force_cache_usd_data/",
    response_model=CacheUsdData,
)
async def force_cache_usd_data():
    usd_data = await saving_usd_to_redis()
    if not usd_data:
        log.error("Can't get usd-data")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return usd_data


@router.get(
    "/get_cached_usd_data/",
    response_model=str | None,
)
async def get_cached_usd_data():
    usd_value = await get_usd_from_redis()

    return usd_value
