import asyncio

import pytest
from fastapi.testclient import TestClient

from api_server.app.app import create_app
from lisichki.domain.usecases.login import LoginUserUseCase
from lisichki.domain.usecases.messages import ManageMessagesUseCase
from lisichki.domain.usecases.registration import (
    RegistrateUserUseCase,
    registration_errors,
)
from lisichki.domain.usecases.roles import ManageRolesUseCase
from lisichki.implementations.message_repository import (
    PostgresMessageRepository,
)
from lisichki.implementations.password_hasher import Argon2PasswordHasher
from lisichki.implementations.token_manager import JwtTokenManager
from lisichki.implementations.user_repository import PostgresUserRepository
from utils.config import Configuration


@pytest.fixture(scope="session")
def client() -> TestClient:
    config = Configuration.from_env()

    password_hasher = Argon2PasswordHasher(
        time_cost=config.argon2.time_cost,
        memory_cost=config.argon2.memory_cost,
        parallelism=config.argon2.parallelism,
    )
    token_manager = JwtTokenManager(
        secret_key=config.jwt.secret_key,
    )
    user_repo = PostgresUserRepository(url=config.database.url)
    message_repo = PostgresMessageRepository(url=config.database.url)

    registrate_user = RegistrateUserUseCase(user_repo, password_hasher, token_manager)
    login_user = LoginUserUseCase(user_repo, password_hasher, token_manager)
    manage_roles = ManageRolesUseCase(user_repo, token_manager)
    manage_messages = ManageMessagesUseCase(message_repo, user_repo, token_manager)

    try:
        asyncio.run(
            registrate_user.registrate_admin(
                login=config.admin.login,
                password=config.admin.password,
            )
        )
    except registration_errors.UserAlreadyExistsError:
        pass

    app = create_app(
        registrate_user=registrate_user,
        login_user=login_user,
        manage_roles=manage_roles,
        manage_messages=manage_messages,
    )

    return TestClient(app)
