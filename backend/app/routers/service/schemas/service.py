from pydantic import BaseModel, Field


class PingResponse(BaseModel):
    message: str = Field(
        example="pong",
    )
