import logging

from fastapi.responses import UJSONResponse
from core.config import settings
from app.routers.service.schemas.service import PingResponse
from app.routers.order.api.order import router as order_router
from app.routers.session.api.session import router as session_router
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app import __version__
from core.database.dbHelper import db

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    log.info("Database is going to be disposed")
    await db.dispose()


main_router = FastAPI(
    title=settings.TITLE,
    version=__version__,
    openapi_url=f"{settings.OPENAPI_PREFIX}/openapi.json",
    root_path=settings.ROOT_PATH,
    default_response_class=UJSONResponse,
    lifespan=lifespan,
)


@main_router.get(
    "/ping/",
    tags=["Service"],
    response_model=PingResponse,
)
async def ping():
    return {"message": "pong"}


main_router.include_router(
    order_router,
    prefix="/api/order",
)

main_router.include_router(
    session_router,
    prefix="/auth",
)
