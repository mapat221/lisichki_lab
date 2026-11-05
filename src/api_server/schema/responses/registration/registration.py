from typing import Self

from pydantic import Field, StrictStr

from api_server.schema.responses.base import SuccessResponse


class RegistrationResponseBody(SuccessResponse):
    message: StrictStr = Field(
        description="Registration status",
        examples=["User registrated"],
    )
    access_token: StrictStr = Field(
        description="User acess token",
        examples=["eyJhbGciOiJIUzI1Ni..."],
    )
    login: StrictStr = Field(
        description="User login",
        examples=["Alfredo"],
    )
    roles: list[StrictStr] = Field(
        description="User roles",
        examples=[["user"]],
    )

    @classmethod
    def create(
        cls,
        message: str,
        access_token: str,
        login: str,
        roles: list[str],
    ) -> Self:
        return cls(
            message=message,
            access_token=access_token,
            login=login,
            roles=roles,
        )
