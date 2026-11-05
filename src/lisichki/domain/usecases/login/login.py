import logging

from lisichki.domain.entities import User
from lisichki.interfaces.password_hasher import PasswordHasher
from lisichki.interfaces.token_manager import TokenManager
from lisichki.interfaces.user_repository import UserRepository

from . import login_errors


class LoginUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        token_manager: TokenManager,
    ) -> None:
        self._user_repository = user_repository
        self._password_hasher = password_hasher
        self._token_manager = token_manager
        self.logger = logging.getLogger(__name__)

    async def login(self, login: str, password: str) -> User:
        user = await self._user_repository.get_by_login(login)
        if user is None:
            self.logger.error(f"Login failed: user {login} not found")
            raise login_errors.UserNotFoundError

        if not self._password_hasher.verify(user.password_hash, password):
            self.logger.error(f"Login failed: invalid password for user {login}")
            raise login_errors.InvalidPasswordError

        token = self._token_manager.create_token(user.login)
        user.token = token
        self.logger.info(f"User {login} successfully logged in")
        return user
