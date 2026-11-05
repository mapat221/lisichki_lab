from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    @abstractmethod
    def hash(self, password: str):
        pass

    @abstractmethod
    def verify(self, hash: str, password: str):
        pass
