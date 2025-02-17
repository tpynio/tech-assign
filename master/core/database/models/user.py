from core.database.base import Base

from core.database.mixins import UUIDPkId, Timestamps


class User(UUIDPkId, Timestamps, Base):
    __tablename__ = "users"
