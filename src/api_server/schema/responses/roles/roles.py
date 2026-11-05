from pydantic import BaseModel, Field, StrictStr
from typing_extensions import Self

from lisichki.domain.entities import Roles


class UserRoleItem(BaseModel):
    login: StrictStr = Field(
        description="User login",
        examples=["Alfredo"],
    )
    roles: list[Roles] = Field(
        description="User roles",
        examples=[[Roles.user, Roles.moderator]],
    )


class GetUsersResponseBody(BaseModel):
    users: list[UserRoleItem]

    @classmethod
    def create(cls, users: list[UserRoleItem]) -> Self:
        return cls(users=users)


class SetRolesResponseBody(BaseModel):
    message: StrictStr = Field(
        description="Set roles status",
        examples=["Roles updated"],
    )
    login: StrictStr = Field(
        description="Target user login",
        examples=["Alfredo"],
    )
    roles: list[Roles] = Field(
        description="Target user roles",
        examples=[[Roles.user, Roles.moderator]],
    )

    @classmethod
    def create(
        cls,
        message: str,
        login: str,
        roles: list[Roles],
    ) -> Self:
        return cls(
            message=message,
            login=login,
            roles=roles,
        )
