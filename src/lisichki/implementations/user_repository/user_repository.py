from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from lisichki.domain.entities import Roles, User
from lisichki.implementations.db.models import RoleOrm, UserOrm
from lisichki.interfaces.user_repository import UserRepository


class PostgresUserRepository(UserRepository):
    def __init__(
        self,
        url: str,
    ) -> None:
        self._engine = create_async_engine(url, poolclass=NullPool)
        self._session_factory = async_sessionmaker(
            self._engine,
            expire_on_commit=False,
        )

    def _to_domain(self, user_orm: UserOrm):
        return User(
            id_=str(user_orm.id),
            login=str(user_orm.login),
            password_hash=str(user_orm.password_hash),
            created_at=user_orm.created_at,
            roles=[Roles(role.name) for role in user_orm.roles],
        )

    async def get_by_login(self, login: str) -> User | None:
        async with self._session_factory() as session:
            request = select(UserOrm).where(UserOrm.login == login)
            user_orm = await session.scalar(request)
            if user_orm is None:
                return None
            return self._to_domain(user_orm)

    async def create(
        self,
        login: str,
        password_hash: str,
        roles: list[Roles],
    ) -> User:
        async with self._session_factory() as session:
            role_names = [role.value for role in roles]
            request = select(RoleOrm).where(RoleOrm.name.in_(role_names))
            role_orms = list(await session.scalars(request))
            user_orm = UserOrm(
                login=login,
                password_hash=password_hash,
                roles=role_orms,
            )
            session.add(user_orm)
            await session.commit()
            return self._to_domain(user_orm)

    async def get_all(self) -> list[User]:
        async with self._session_factory() as session:
            request = select(UserOrm).order_by(UserOrm.id)
            user_orms = (await session.scalars(request)).all()
            return [self._to_domain(user) for user in user_orms]

    async def update_roles(
        self,
        login: str,
        roles: list[Roles],
    ) -> User | None:
        async with self._session_factory() as session:
            user_request = select(UserOrm).where(UserOrm.login == login)
            user_orm = await session.scalar(user_request)
            if user_orm is None:
                return None
            role_names = [role.value for role in roles]
            role_request = select(RoleOrm).where(RoleOrm.name.in_(role_names))
            role_orms = list(await session.scalars(role_request))
            user_orm.roles = role_orms
            await session.commit()
            return self._to_domain(user_orm)
