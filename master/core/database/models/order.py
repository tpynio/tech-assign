from core.database.base import Base
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from core.database.mixins import PlainPkId, Timestamps
from core.database.models.user import User
import uuid


OrderTypes: list[str] = [
    "Clothes",
    "Electronics",
    "Misc",
]


class OrderType(PlainPkId, Base):
    __tablename__ = "order_types"
    name: Mapped[str] = mapped_column(String(16), unique=True)


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
    deliver_id: Mapped[int] = mapped_column(Integer)

    user_id: Mapped[uuid.UUID.hex] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(
        "User",
        lazy="joined",
    )

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
