from core.database.base import Base
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates


OrderTypes: list[str] = [
    "Clothes",
    "Electronics",
    "Misc",
]


class OrderType(Base):
    __tablename__ = "order_types"
    name: Mapped[str] = mapped_column(String(16), unique=True)


class Order(Base):
    __tablename__ = "orders"

    name: Mapped[str] = mapped_column(String(64))
    type_id: Mapped[int] = mapped_column(ForeignKey("order_types.id"))
    type: Mapped["OrderType"] = relationship(
        "Type", back_populates="orders", lazy="joined"  # autojoin while get order
    )
    weight: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)
    deliver_id: Mapped[int] = mapped_column(Integer)

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
