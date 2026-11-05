from pydantic import BaseModel, Field, StrictStr
from typing_extensions import Self


class LoginResponseBody(BaseModel):
    message: StrictStr = Field(
        description="Login status",
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
