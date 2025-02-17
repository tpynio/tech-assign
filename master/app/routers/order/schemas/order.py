from core.database.models.order import OrderTypes
from pydantic import BaseModel, Field, field_validator
from typing import Literal


class RegisterOrderParams(BaseModel):
    name: str = Field(..., description="Наименование посылки")
    weight: int = Field(..., description="Вес посылки")
    type: Literal[*OrderTypes] = Field(..., description="Тип посылки")
    price: int = Field(..., description="Стоимость посылки")

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


class RegisterOrderResponse(BaseModel):
    order_id: int = Field(
        example="1",
    )
