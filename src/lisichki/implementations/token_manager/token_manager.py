import jwt

from lisichki.interfaces.token_manager import TokenManager

from . import token_manager_errors


class JwtTokenManager(TokenManager):
    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
    ) -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm

    def create_token(self, login: str) -> str:
        payload = {"sub": login}
        return jwt.encode(
            payload,
            self._secret_key,
            algorithm=self._algorithm,
        )

    def get_login_from_token(self, token: str) -> str:
        try:
            payload = jwt.decode(
                token,
                self._secret_key,
                algorithms=[self._algorithm],
            )
            login = payload.get("sub")
            if not isinstance(login, str):
                raise token_manager_errors.InvalidTokenError
            return login
        except jwt.PyJWTError as exc:
            raise token_manager_errors.InvalidTokenError from exc
