import logging

from lisichki.domain.entities import Message, Roles, User
from lisichki.implementations.token_manager import token_manager_errors
from lisichki.interfaces.message_repository import MessageRepository
from lisichki.interfaces.token_manager import TokenManager
from lisichki.interfaces.user_repository import UserRepository

from . import messages_errors


class ManageMessagesUseCase:
    def __init__(
        self,
        message_repository: MessageRepository,
        user_repository: UserRepository,
        token_manager: TokenManager,
    ) -> None:
        self._message_repository = message_repository
        self._user_repository = user_repository
        self._token_manager = token_manager
        self.logger = logging.getLogger(__name__)

    async def _get_caller(self, token: str) -> User:
        try:
            caller_login = self._token_manager.get_login_from_token(token)
        except token_manager_errors.InvalidTokenError as exc:
            self.logger.error("Invalid token provided")
            raise messages_errors.UnauthorizedError from exc
        caller = await self._user_repository.get_by_login(caller_login)
        if caller is None:
            self.logger.error(f"Caller {caller_login} not found")
            raise messages_errors.UnauthorizedError
        return caller

    async def get_all_messages(self, token: str) -> list[Message]:
        await self._get_caller(token)
        return await self._message_repository.get_all()

    async def send_message(self, token: str, text: str) -> Message:
        caller = await self._get_caller(token)
        if not text.strip():
            self.logger.error("Message text can not be empty")
            raise messages_errors.EmptyMessageError
        message = await self._message_repository.create(
            author_login=caller.login,
            text=text,
        )
        self.logger.info(f"User {caller.login} sent message {message.id_}")
        return message

    async def delete_message(self, token: str, message_id: int) -> None:
        caller = await self._get_caller(token)
        if Roles.moderator not in caller.roles and Roles.admin not in caller.roles:
            self.logger.error(
                f"Access denied: user {caller.login} cannot delete messages"
            )
            raise messages_errors.PermissionDeniedError
        deleted = await self._message_repository.delete(message_id)
        if not deleted:
            self.logger.error(f"Message {message_id} not found")
            raise messages_errors.MessageNotFoundError
        self.logger.info(f"User {caller.login} deleted message {message_id}")
