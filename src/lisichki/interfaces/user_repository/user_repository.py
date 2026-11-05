from abc import ABC, abstractmethod

from lisichki.domain.entities import Roles, User


class UserRepository(ABC):
    @abstractmethod
    async def create(self, login: str, password_hash: str, roles: list[Roles]) -> User:
        pass

    @abstractmethod
    async def get_by_login(self, login: str) -> User | None:
        pass

    @abstractmethod
    async def get_all(self) -> list[User]:
        pass

    @abstractmethod
    async def update_roles(self, login: str, roles: list[Roles]) -> User | None:
        pass
