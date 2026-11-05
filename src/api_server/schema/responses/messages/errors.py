from pydantic import BaseModel, Field, StrictStr
from typing_extensions import Self


class UnauthorizedResponseBody(BaseModel):
    detail: StrictStr = Field(
        description="Error detail",
        examples=["Unauthorized"],
    )

    @classmethod
    def new(cls, detail: str) -> Self:
        return cls(detail=detail)


class PermissionDeniedResponseBody(BaseModel):
    detail: StrictStr = Field(
        description="Error detail",
        examples=["Access denied for caller"],
    )

    @classmethod
    def new(cls, detail: str) -> Self:
        return cls(detail=detail)


class MessageNotFoundResponseBody(BaseModel):
    detail: StrictStr = Field(
        description="Error detail",
        examples=["Message not found"],
    )

    @classmethod
    def new(cls, detail: str) -> Self:
        return cls(detail=detail)


class EmptyMessageResponseBody(BaseModel):
    detail: StrictStr = Field(
        description="Error detail",
        examples=["Message text can not be empty"],
    )

    @classmethod
    def new(cls, detail: str) -> Self:
        return cls(detail=detail)
