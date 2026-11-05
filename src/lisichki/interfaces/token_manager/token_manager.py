from abc import ABC, abstractmethod


class TokenManager(ABC):
    @abstractmethod
    def create_token(self, login: str) -> str:
        pass

    @abstractmethod
    def get_login_from_token(self, token: str) -> str:
        pass
