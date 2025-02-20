from pydantic import BaseModel, Field


class CachedUSDData(BaseModel):
    ID: str = Field(..., examples=["R01235"])
    NumCode: str = Field(..., examples=["840"])
    CharCode: str = Field(..., examples=["USD"])
    Name: str = Field(..., examples=["Доллар США"])
    Value: float = Field(..., examples=[91.3398])
    Previous: float = Field(..., examples=[91.4347])


class CachedUSDValue(BaseModel):
    value: str


class ForceRecalculate(BaseModel):
    status: str
