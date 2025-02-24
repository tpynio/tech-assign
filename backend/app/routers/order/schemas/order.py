from typing import Literal, Optional

from core.database.models.order import OrderTypes
from fastapi_pagination import Page
from pydantic import BaseModel, Field, field_validator


class FilterParams(BaseModel):
    filterByType: Optional[Literal[*OrderTypes]] = Field(
        None, description="Фильтрация по типу"
    )
    deliveryPriceIsNull: Optional[bool] = Field(
        None, description="Фильтрация по наличию расчитанной стоимости"
    )


class Order(BaseModel):
    name: str = Field(..., description="Наименование посылки", examples=["socks"])
    weight: float = Field(..., description="Вес посылки, в кг", examples=[0.5, 1.2])
    type: Literal[*OrderTypes] = Field(
        ..., description="Тип посылки", examples=["Clothes"]
    )
    price: float = Field(
        ..., description="Стоимость посылки, в долларах", examples=[1.99, 1]
    )


class RegisterOrderParams(Order):
    @field_validator("weight")
    @classmethod
    def weight_validator(cls, weight_value: int):
        if weight_value < 0:
            raise ValueError("weight must be greater or equal than 0")
        return weight_value

    @field_validator("price")
    @classmethod
    def price_validator(cls, price_value: int):
        if price_value <= 0:
            raise ValueError("price_value must be greater or equal than 0")
        return price_value

    @field_validator("type")
    @classmethod
    def type_validator(cls, type_value: str):
        if type_value not in OrderTypes:
            raise ValueError(
                f"type should be one of the following: {', '.join(OrderTypes)}"
            )
        return type_value


class OrderResponse(Order):
    order_id: int = Field(..., description="id заказа пользователя")
    delivery_price: float | str = Field(
        None, description="Расчитанная стоимость доставки, в рублях", examples=[120.45]
    )


class OrderType(BaseModel):
    id: int = Field(..., description="id типа заказа")
    name: str = Field(
        ...,
        description="наименование типа заказа",
        examples=["Clothes", "Electronics", "Misc"],
    )


class OrdersPaginateResponse(Page):
    items: list[OrderResponse]
