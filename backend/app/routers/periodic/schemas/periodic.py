from pydantic import BaseModel, Field


class CacheUsdData(BaseModel):
    ID: str = Field(..., examples=["R01235"])
    NumCode: str = Field(..., examples=["840"])
    CharCode: str = Field(..., examples=["USD"])
    Nominal: int = (Field(..., examples=[1]),)
    Name: str = Field(..., examples=["Доллар США"])
    Value: float = Field(..., examples=[91.3398])
    Previous: float = Field(..., examples=[91.4347])
