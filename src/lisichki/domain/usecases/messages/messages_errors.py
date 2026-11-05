class MessagesError(Exception):
    pass


class UnauthorizedError(MessagesError):
    pass


class PermissionDeniedError(MessagesError):
    pass


class MessageNotFoundError(MessagesError):
    pass


class EmptyMessageError(MessagesError):
    pass
