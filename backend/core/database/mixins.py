import uuid
from datetime import datetime

from sqlalchemy import UUID, Integer, func
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy.orm import Mapped, mapped_column


class PlainPkId:
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class UUIDPkId:
    """
    MySQL позволяет хранить UUID в виде BINARY(16), что хорошо для индексации такого ключа,
    лучше и должно быть сильно быстрее чем работа с UUID в сиде строку
    """

    id: Mapped[UUID] = mapped_column(
        BINARY(16), primary_key=True, default=lambda: uuid.uuid4().bytes
    )


class Timestamps:
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
