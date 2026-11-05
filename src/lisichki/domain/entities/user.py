from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class Roles(Enum):
    user = "user"
    moderator = "moderator"
    admin = "admin"


class User(BaseModel):
    id_: str
    login: str
    created_at: datetime
    password_hash: str
    roles: list[Roles]
    token: str = ""
