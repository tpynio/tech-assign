import logging

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from core.config import settings
from app.routers.schemas.service import PingResponse
from app import __version__

log = logging.getLogger(__name__)

app = FastAPI(
    title=settings.TITLE,
    version=__version__,
    openapi_url=f"{settings.OPENAPI_PREFIX}/openapi.json",
    root_path=settings.ROOT_PATH,
    default_response_class=UJSONResponse,
)


@app.get(
    "/ping/",
    tags=["Service"],
    response_model=PingResponse,
)
def ping():
    return {"message": "pong"}
