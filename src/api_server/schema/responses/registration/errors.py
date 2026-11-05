from typing import Self

from pydantic import BaseModel, Field, StrictStr


class UserAlreadyExistsResponseBody(BaseModel):
    detail: StrictStr = Field(
        description="Error detail",
        examples=["User already exists"],
    )

    @classmethod
    def new(cls, detail: str) -> Self:
        return cls(detail=detail)


class InvalidLoginResponseBody(BaseModel):
    detail: StrictStr = Field(
        description="Error detail",
        examples=["User login is invalid"],
    )

    @classmethod
    def new(cls, detail: str) -> Self:
        return cls(detail=detail)


class WeakPasswordResponseBody(BaseModel):
    detail: StrictStr = Field(
        description="Error detail",
        examples=["User password is so weak"],
    )

    @classmethod
    def new(cls, detail: str) -> Self:
        return cls(detail=detail)
