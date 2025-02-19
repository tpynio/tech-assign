from core.database.base import Base

from core.database.mixins import UUIDPkId, Timestamps
import uuid


class User(UUIDPkId, Timestamps, Base):
    __tablename__ = "users"

    def to_dict(self):
        return {
            "id": uuid.UUID(bytes=self.id),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
