from pydantic import BaseModel, Field


class CachedUSDValue(BaseModel):
    value: str = Field(..., description="Курс рубля к доллару", examples=[91.3398])


class ForcePeriodicTask(BaseModel):
    status: str = Field(..., description="Статус запуска задачи", examples=["success"])
