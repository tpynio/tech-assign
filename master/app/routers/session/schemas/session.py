from pydantic import BaseModel, Field


class SessionResponse(BaseModel):
    result: str | None = Field(
        ...,
        description="Session id",
        example="f7caf19cdc034a918af12d440cf10a7f",
    )
