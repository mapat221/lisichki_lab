import asyncio
import logging
import os

import environment as env
from api_server.app.app import create_app, start_api_server
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

LOGGER = logging.getLogger(__name__)


def main() -> int:
    try:
        config = Configuration.from_env()
    except Exception:
        LOGGER.critical("Unable to obtain configuration.", exc_info=True)
        return 1

    password_hasher = Argon2PasswordHasher(
        time_cost=config.argon2.time_cost,
        memory_cost=config.argon2.memory_cost,
        parallelism=config.argon2.parallelism,
    )
    token_manager = JwtTokenManager(
        secret_key=config.jwt.secret_key,
    )
    user_repository = PostgresUserRepository(
        url=config.database.url,
    )
    message_repository = PostgresMessageRepository(
        url=config.database.url,
    )

    registrate_user = RegistrateUserUseCase(
        user_repository=user_repository,
        password_hasher=password_hasher,
        token_manager=token_manager,
    )
    login_user = LoginUserUseCase(
        user_repository=user_repository,
        password_hasher=password_hasher,
        token_manager=token_manager,
    )
    manage_roles = ManageRolesUseCase(
        user_repository=user_repository,
        token_manager=token_manager,
    )
    manage_messages = ManageMessagesUseCase(
        message_repository=message_repository,
        user_repository=user_repository,
        token_manager=token_manager,
    )

    try:
        asyncio.run(
            registrate_user.registrate_admin(
                login=config.admin.login,
                password=config.admin.password,
            )
        )
    except registration_errors.UserAlreadyExistsError:
        LOGGER.info("Admin user already exists, skip")
    except registration_errors.InvalidLoginError:
        LOGGER.critical("Admin login is invalid")
        return 1
    except registration_errors.WeakPasswordError:
        LOGGER.critical("Admin password is weak")
        return 1
    except Exception:
        LOGGER.critical("Unable to create admin user.", exc_info=True)
        return 1

    web_app = create_app(
        registrate_user=registrate_user,
        login_user=login_user,
        manage_roles=manage_roles,
        manage_messages=manage_messages,
    )

    try:
        start_api_server(web_app, host="0.0.0.0", port=env.SERVE_PORT)
    except Exception:
        LOGGER.critical("API server stopped with error.", exc_info=True)
        return 1

    return 0


if __name__ == "__main__":
    exit_code = main()
    os._exit(exit_code)
