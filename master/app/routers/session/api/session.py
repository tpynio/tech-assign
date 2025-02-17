from typing import Any
import uuid
from time import time
from fastapi import APIRouter, HTTPException, status, Response, Request
from core.config import settings

router = APIRouter(
    tags=["Session"],
)

COOKIES: dict[str, dict[str, Any]] = {}


def generate_session_id() -> str:
    return uuid.uuid4().hex


@router.post("/session/")
async def create_session(response: Response):
    session_id = generate_session_id()
    response.set_cookie(settings.COOKIE_SESSION_ID_KEY_NAME, session_id)
    COOKIES[session_id] = {"user": session_id, "loginAt": int(time())}
    return {"result": "ok"}


@router.get("/session/")
async def whoami(
    request: Request,
):
    session_id = request.cookies.get(settings.COOKIE_SESSION_ID_KEY_NAME)
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="not authenticated"
        )
    return COOKIES[session_id]


@router.delete("/session/")
async def delete_session(
    request: Request,
    response: Response,
):
    session_id = request.cookies.get(settings.COOKIE_SESSION_ID_KEY_NAME)
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="not authenticated"
        )
    COOKIES.pop(session_id)
    response.delete_cookie(settings.COOKIE_SESSION_ID_KEY_NAME)
    return {"result": "success"}
