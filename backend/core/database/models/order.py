import uuid

from core.database.base import Base
from core.database.mixins import PlainPkId, Timestamps
from core.database.models.user import User
from sqlalchemy import UUID, ForeignKey, Integer, String
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

OrderTypes: list[str] = [
    "Clothes",
    "Electronics",
    "Misc",
]


class OrderType(PlainPkId, Base):
    __tablename__ = "order_types"
    name: Mapped[str] = mapped_column(String(16), unique=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class Order(PlainPkId, Timestamps, Base):
    __tablename__ = "orders"

    name: Mapped[str] = mapped_column(String(64))
    type_id: Mapped[int] = mapped_column(ForeignKey("order_types.id"))
    order_type: Mapped["OrderType"] = relationship(
        "OrderType",
        lazy="joined",  # autojoin while get order
    )
    weight: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)
    deliver_id: Mapped[int | None] = mapped_column(
        Integer, nullable=True, server_default=None
    )

    user_id: Mapped[UUID] = mapped_column(
        BINARY(16), ForeignKey("users.id", ondelete="CASCADE")
    )
    user: Mapped["User"] = relationship(
        "User",
        lazy="joined",
    )
    delivery_price: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type_id": self.type_id,
            "user_id": uuid.UUID(bytes=self.user_id),
            "weight": self.weight,
            "price": self.price,
            "deliver_id": self.deliver_id,
            "delivery_price": self.delivery_price,
        }

    @validates("weight")
    def weight_validator(self, key, weight_value):
        if weight_value < 0:
            raise ValueError("weight must be greater or equal than 0")
        return weight_value

    @validates("price")
    def price_validator(self, key, price_value):
        if price_value <= 0:
            raise ValueError("price must be greater than 0")
        return price_value
