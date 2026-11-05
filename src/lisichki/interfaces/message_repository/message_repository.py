from abc import ABC, abstractmethod

from lisichki.domain.entities import Message


class MessageRepository(ABC):
    @abstractmethod
    async def create(self, author_login: str, text: str) -> Message:
        pass

    @abstractmethod
    async def get_all(self) -> list[Message]:
        pass

    @abstractmethod
    async def delete(self, message_id: int) -> bool:
        pass
