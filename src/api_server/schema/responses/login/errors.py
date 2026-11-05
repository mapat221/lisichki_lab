from pydantic import BaseModel, Field, StrictStr
from typing_extensions import Self


class UserNotFoundResponseBody(BaseModel):
    detail: StrictStr = Field(
        description="Error detail",
        examples=["User not found"],
    )

    @classmethod
    def new(cls, detail: str) -> Self:
        return cls(detail=detail)


class InvalidPasswordResponseBody(BaseModel):
    detail: StrictStr = Field(
        description="Error detail",
        examples=["Invalid password for user"],
    )

    @classmethod
    def new(cls, detail: str) -> Self:
        return cls(detail=detail)
