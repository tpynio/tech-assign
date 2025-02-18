import logging

from fastapi import Depends, Request, Response, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from core.database.dbHelper import db
from core.database.models.user import User
from core.config import settings
import uuid

log = logging.getLogger(__name__)


async def create_user(db_session: AsyncSession, response: Response) -> User:
    user = User()
    db_session.add(user)
    try:
        await db_session.commit()
        await db_session.refresh(user)
    except SQLAlchemyError as exc:
        log.error("Database error", exc_info=exc)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    response.set_cookie(
        settings.COOKIE_SESSION_ID_KEY_NAME, uuid.UUID(bytes=user.id).hex
    )
    return user


async def get_or_make_auth_user(
    request: Request,
    response: Response,
    db_session: AsyncSession = Depends(db.get_session),
) -> User:
    """
    Получение или создание пользователя с записью в куки
    :param request: запрос из которого хочется взять куки
    :param response: ответ в который по необходимости нужно засыпать новые куки
    :param db_session: сессия в бд
    :return: новый или тотже пользователь
    """
    session_id = request.cookies.get(settings.COOKIE_SESSION_ID_KEY_NAME)

    if not session_id:
        user = await create_user(db_session, response)

        return user

    user: User | None = await db_session.get(User, uuid.UUID(session_id).bytes)
    if not user:
        user = await create_user(db_session, response)

    return user
