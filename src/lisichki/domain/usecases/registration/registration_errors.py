class RegistrationError(Exception):
    pass


class UserAlreadyExistsError(RegistrationError):
    pass


class InvalidLoginError(RegistrationError):
    pass


class WeakPasswordError(RegistrationError):
    pass
