from typing import Annotated

from fastapi import APIRouter, Header, status
from fastapi.responses import JSONResponse

from api_server import schema
from api_server.app import dependency
from lisichki.domain.usecases.messages import messages_errors

messages_router = APIRouter(
    prefix="/api",
    tags=["messages"],
)


@messages_router.get(
    "/messages",
    status_code=status.HTTP_200_OK,
    response_model=schema.responses.messages.GetMessagesResponseBody,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": schema.responses.messages.errors.UnauthorizedResponseBody
        },
    },
)
async def get_messages(
    token: Annotated[str, Header()],
) -> schema.responses.messages.GetMessagesResponseBody | JSONResponse:
    try:
        messages = await dependency.manage_messages.get_all_messages(token=token)
    except messages_errors.UnauthorizedError:
        detail = "Unauthorized"
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=schema.responses.messages.errors.UnauthorizedResponseBody.new(
                detail=detail
            ).model_dump(),
        )
    items = [
        schema.responses.messages.MessageItem(
            id_=message.id_,
            author_login=message.author_login,
            text=message.text,
            created_at=message.created_at,
        )
        for message in messages
    ]
    return schema.responses.messages.GetMessagesResponseBody.create(messages=items)


@messages_router.post(
    "/messages",
    status_code=status.HTTP_201_CREATED,
    response_model=schema.responses.messages.SendMessageResponseBody,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": schema.responses.messages.errors.UnauthorizedResponseBody
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": schema.responses.messages.errors.EmptyMessageResponseBody
        },
    },
)
async def send_message(
    token: Annotated[str, Header()],
    body: schema.requests.messages.SendMessageRequestBody,
) -> schema.responses.messages.SendMessageResponseBody | JSONResponse:
    try:
        msg = await dependency.manage_messages.send_message(
            token=token,
            text=body.text,
        )
    except messages_errors.UnauthorizedError:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=schema.responses.messages.errors.UnauthorizedResponseBody.new(
                detail="Unauthorized"
            ).model_dump(),
        )
    except messages_errors.EmptyMessageError:
        detail = "Message text can not be empty"
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=schema.responses.messages.errors.EmptyMessageResponseBody.new(
                detail=detail
            ).model_dump(),
        )
    item = schema.responses.messages.MessageItem(
        id_=msg.id_,
        author_login=msg.author_login,
        text=msg.text,
        created_at=msg.created_at,
    )
    message = item
    return schema.responses.messages.SendMessageResponseBody.create(message=message)


@messages_router.delete(
    "/messages/{message_id}",
    status_code=status.HTTP_200_OK,
    response_model=schema.responses.messages.DeleteMessageResponseBody,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": schema.responses.messages.errors.UnauthorizedResponseBody
        },
        status.HTTP_403_FORBIDDEN: {
            "model": schema.responses.messages.errors.PermissionDeniedResponseBody
        },
        status.HTTP_404_NOT_FOUND: {
            "model": schema.responses.messages.errors.MessageNotFoundResponseBody
        },
    },
)
async def delete_message(
    token: Annotated[str, Header()],
    message_id: int,
) -> schema.responses.messages.DeleteMessageResponseBody | JSONResponse:
    try:
        await dependency.manage_messages.delete_message(
            token=token,
            message_id=message_id,
        )
    except messages_errors.UnauthorizedError:
        detail = "Unauthorized"
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=schema.responses.messages.errors.UnauthorizedResponseBody.new(
                detail=detail
            ).model_dump(),
        )
    except messages_errors.PermissionDeniedError:
        detail = "Access denied for caller"
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=schema.responses.messages.errors.PermissionDeniedResponseBody.new(
                detail=detail
            ).model_dump(),
        )
    except messages_errors.MessageNotFoundError:
        detail = "Message not found"
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=schema.responses.messages.errors.MessageNotFoundResponseBody.new(
                detail=detail
            ).model_dump(),
        )
    message = "Message deleted"
    return schema.responses.messages.DeleteMessageResponseBody.create(message=message)
