class LoginError(Exception):
    pass


class UserNotFoundError(LoginError):
    pass


class InvalidPasswordError(LoginError):
    pass
