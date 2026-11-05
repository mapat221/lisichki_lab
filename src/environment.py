import os

APP_ENV: str = os.getenv("APP_ENV", "development")

DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/lisichki_db",
)

HASH_SCHEME: str = os.getenv("HASH_SCHEME", "argon2id")
ARGON2_TIME_COST: int = int(os.getenv("ARGON2_TIME_COST", "3"))
ARGON2_MEMORY_COST: int = int(os.getenv("ARGON2_MEMORY_COST", "65536"))
ARGON2_PARALLELISM: int = int(os.getenv("ARGON2_PARALLELISM", "4"))

ADMIN_LOGIN: str = os.getenv("ADMIN_LOGIN", "admin")
ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "Abcd123456!")

SECRET_KEY: str = os.getenv(
    "SECRET_KEY",
    "ddb7203e99d999bf02093109ce948a41bf3e5e3797b01a7d1b550f92ba535cb9",
)

SERVE_PORT: int = int(os.getenv("PORT", "8000"))
