from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from lisichki.domain.entities import Message
from lisichki.implementations.db.models import MessageOrm
from lisichki.interfaces.message_repository import MessageRepository


class PostgresMessageRepository(MessageRepository):
    def __init__(
        self,
        url: str,
    ) -> None:
        self._engine = create_async_engine(url, poolclass=NullPool)
        self._session_factory = async_sessionmaker(
            self._engine,
            expire_on_commit=False,
        )

    def _to_domain(self, message_orm: MessageOrm) -> Message:
        return Message(
            id_=str(message_orm.id),
            author_login=str(message_orm.author_login),
            text=str(message_orm.text),
            created_at=message_orm.created_at,
        )

    async def create(
        self,
        author_login: str,
        text: str,
    ) -> Message:
        async with self._session_factory() as session:
            message_orm = MessageOrm(
                author_login=author_login,
                text=text,
            )
            session.add(message_orm)
            await session.commit()
            return self._to_domain(message_orm)

    async def get_all(self) -> list[Message]:
        async with self._session_factory() as session:
            request = select(MessageOrm).order_by(MessageOrm.id)
            message_orms = (await session.scalars(request)).all()
            return [self._to_domain(message) for message in message_orms]

    async def delete(
        self,
        message_id: int,
    ) -> bool:
        async with self._session_factory() as session:
            request = select(MessageOrm).where(MessageOrm.id == message_id)
            message_orm = await session.scalar(request)
            if message_orm is None:
                return False
            await session.delete(message_orm)
            await session.commit()
            return True
