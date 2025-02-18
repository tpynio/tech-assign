from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, status, Response, Request, Depends
from core.config import settings
from app.routers.session.schemas.session import SessionResponse
from app.routers.session.crud.session import create_session, get_session, del_session
from core.database.dbHelper import db


router = APIRouter(
    tags=["Session"],
)


@router.post(
    "/session/",
    response_model=SessionResponse,
)
async def make_session(
    request: Request,
    response: Response,
    db_session: AsyncSession = Depends(db.get_session),
):
    session_id = request.cookies.get(settings.COOKIE_SESSION_ID_KEY_NAME)
    new_session_id = await create_session(db_session=db_session, session_id=session_id)
    response.set_cookie(settings.COOKIE_SESSION_ID_KEY_NAME, new_session_id)
    return {"result": new_session_id}


@router.get(
    "/session/",
    response_model=SessionResponse,
)
async def whoami(
    request: Request,
    db_session: AsyncSession = Depends(db.get_session),
):
    session_id = request.cookies.get(settings.COOKIE_SESSION_ID_KEY_NAME)
    check_session_id = await get_session(db_session=db_session, session_id=session_id)

    if not check_session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="not authenticated"
        )
    return {"result": check_session_id}


@router.delete(
    "/session/",
    response_model=SessionResponse,
)
async def delete_session(
    request: Request,
    response: Response,
    db_session: AsyncSession = Depends(db.get_session),
):
    session_id = request.cookies.get(settings.COOKIE_SESSION_ID_KEY_NAME)
    await del_session(db_session=db_session, session_id=session_id)
    response.delete_cookie(settings.COOKIE_SESSION_ID_KEY_NAME)
    return {"result": None}
