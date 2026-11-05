class RolesError(Exception):
    pass


class UnauthorizedError(RolesError):
    pass


class PermissionDeniedError(RolesError):
    pass


class UserNotFoundError(RolesError):
    pass


class CannotModifyAdminError(RolesError):
    pass
