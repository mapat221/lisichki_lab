from typing import Self

from pydantic import BaseModel, StrictInt, StrictStr

import environment as env


class Configuration(BaseModel):
    class Argon2Config(BaseModel):
        time_cost: StrictInt
        memory_cost: StrictInt
        parallelism: StrictInt

    class DatabaseConfig(BaseModel):
        url: StrictStr

    class AdminConfig(BaseModel):
        login: StrictStr
        password: StrictStr

    class JwtConfig(BaseModel):
        secret_key: StrictStr

    argon2: Argon2Config
    database: DatabaseConfig
    admin: AdminConfig
    jwt: JwtConfig

    @classmethod
    def from_env(cls) -> Self:
        return cls(
            argon2=cls.Argon2Config(
                time_cost=env.ARGON2_TIME_COST,
                memory_cost=env.ARGON2_MEMORY_COST,
                parallelism=env.ARGON2_PARALLELISM,
            ),
            database=cls.DatabaseConfig(url=env.DATABASE_URL),
            admin=cls.AdminConfig(login=env.ADMIN_LOGIN, password=env.ADMIN_PASSWORD),
            jwt=cls.JwtConfig(secret_key=env.SECRET_KEY),
        )
