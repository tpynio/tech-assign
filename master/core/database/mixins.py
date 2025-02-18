from datetime import datetime
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy import Integer, func
from sqlalchemy.orm import Mapped, mapped_column
import uuid


class PlainPkId:
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class UUIDPkId:
    id: Mapped[uuid.UUID.hex] = mapped_column(
        BINARY(16), primary_key=True, default=lambda: uuid.uuid4().bytes
    )


class Timestamps:
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
