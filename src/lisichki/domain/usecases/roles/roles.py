import logging

from lisichki.domain.entities import Roles, User
from lisichki.implementations.token_manager import token_manager_errors
from lisichki.interfaces.token_manager import TokenManager
from lisichki.interfaces.user_repository import UserRepository

from . import roles_errors


class ManageRolesUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        token_manager: TokenManager,
    ) -> None:
        self._user_repository = user_repository
        self._token_manager = token_manager
        self.logger = logging.getLogger(__name__)

    async def _get_caller(self, token: str) -> User:
        try:
            caller_login = self._token_manager.get_login_from_token(token)
        except token_manager_errors.InvalidTokenError as exc:
            self.logger.error("Invalid token provided")
            raise roles_errors.UnauthorizedError from exc
        caller = await self._user_repository.get_by_login(caller_login)
        if caller is None:
            self.logger.error(f"Caller {caller_login} not found")
            raise roles_errors.UnauthorizedError
        return caller

    async def get_all_users(self, token: str) -> list[User]:
        caller = await self._get_caller(token)
        if Roles.admin not in caller.roles:
            self.logger.error(f"Access denied for user {caller.login}")
            raise roles_errors.PermissionDeniedError
        return await self._user_repository.get_all()

    async def set_roles(
        self,
        token: str,
        target_login: str,
        roles: list[Roles],
    ) -> User:
        caller = await self._get_caller(token)
        if Roles.admin not in caller.roles:
            self.logger.error(f"Access denied for user {caller.login}")
            raise roles_errors.PermissionDeniedError
        if Roles.admin in roles:
            self.logger.error("Cannot assign admin role")
            raise roles_errors.CannotModifyAdminError
        target_user = await self._user_repository.get_by_login(target_login)
        if target_user is None:
            self.logger.error(f"Target user {target_login} not found")
            raise roles_errors.UserNotFoundError
        if Roles.admin in target_user.roles:
            self.logger.error(f"Target user {target_login} is admin")
            raise roles_errors.CannotModifyAdminError
        updated_user = await self._user_repository.update_roles(
            login=target_login,
            roles=roles,
        )
        if updated_user is None:
            self.logger.error(f"Target user {target_login} not found")
            raise roles_errors.UserNotFoundError
        self.logger.info(f"Admin {caller.login} updated roles for {target_login}")
        return updated_user
