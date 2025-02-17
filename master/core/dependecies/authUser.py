from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from core.database.dbHelper import db
from core.database.models.user import User


async def prefetch_auth_user(
    request: Request,
    db_session: AsyncSession = Depends(db.get_session),
) -> User:
    pass
