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


class UserNotFoundResponseBody(BaseModel):
    detail: StrictStr = Field(
        description="Error detail",
        examples=["Target user not found"],
    )

    @classmethod
    def new(cls, detail: str) -> Self:
        return cls(detail=detail)


class CannotModifyAdminResponseBody(BaseModel):
    detail: StrictStr = Field(
        description="Error detail",
        examples=["Cannot modify admin roles"],
    )

    @classmethod
    def new(cls, detail: str) -> Self:
        return cls(detail=detail)
