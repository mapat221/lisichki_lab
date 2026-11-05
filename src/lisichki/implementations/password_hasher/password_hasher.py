from argon2 import PasswordHasher as ArgonEngine
from argon2 import Type
from argon2.exceptions import VerifyMismatchError

from lisichki.interfaces.password_hasher import PasswordHasher


class Argon2PasswordHasher(PasswordHasher):
    def __init__(
        self,
        time_cost: int,
        memory_cost: int,
        parallelism: int,
    ) -> None:
        self._hasher = ArgonEngine(
            time_cost=time_cost,
            memory_cost=memory_cost,
            parallelism=parallelism,
            type=Type.ID,
        )

    def hash(self, password: str) -> str:
        return self._hasher.hash(password)

    def verify(self, hash: str, password: str):
        try:
            return self._hasher.verify(hash, password)
        except VerifyMismatchError:
            return False
