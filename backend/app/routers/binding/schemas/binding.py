from app.routers.order.schemas.order import OrderResponse
from pydantic import BaseModel, Field, field_validator


class BindingOrderParams(BaseModel):
    delivery_id: int = Field(..., description="id компании доставщика")

    @field_validator("delivery_id")
    @classmethod
    def delivery_id_validator(cls, delivery_id: int):
        if delivery_id <= 0:
            raise ValueError("delivery_id must be positive value")
        return delivery_id


class BindingOrderResponse(OrderResponse):
    delivery_id: int = Field(..., description="id компании доставщика")
