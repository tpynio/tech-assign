import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from core.database.models.user import User


async def create_session(
    db_session: AsyncSession, session_id: str | None = None
) -> str:
    if not session_id:
        user = User()
        db_session.add(user)
        await db_session.commit()
        return uuid.UUID(bytes=user.id).hex
    return session_id


async def get_session(db_session: AsyncSession, session_id: str | None) -> str | None:
    if not session_id:
        return None
    user = await db_session.get(User, uuid.UUID(session_id).bytes)
    if user:
        return session_id
    return None


async def del_session(db_session: AsyncSession, session_id: str | None):
    if not session_id:
        return
    user = await db_session.get(User, uuid.UUID(session_id).bytes)
    if user:
        await db_session.delete(user)
    return
