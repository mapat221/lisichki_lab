from typing import Annotated

from fastapi import APIRouter, Header, status
from fastapi.responses import JSONResponse

from api_server import schema
from api_server.app import dependency
from lisichki.domain.usecases.roles import roles_errors

roles_router = APIRouter(
    prefix="/api",
    tags=["roles"],
)


@roles_router.get(
    "/users",
    status_code=status.HTTP_200_OK,
    response_model=schema.responses.roles.GetUsersResponseBody,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": schema.responses.roles.errors.UnauthorizedResponseBody
        },
        status.HTTP_403_FORBIDDEN: {
            "model": schema.responses.roles.errors.PermissionDeniedResponseBody
        },
    },
)
async def get_users(
    token: Annotated[str, Header()],
) -> schema.responses.roles.GetUsersResponseBody | JSONResponse:
    try:
        users = await dependency.manage_roles.get_all_users(token=token)
    except roles_errors.UnauthorizedError:
        detail = "Unauthorized"
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=schema.responses.roles.errors.UnauthorizedResponseBody.new(
                detail=detail
            ).model_dump(),
        )
    except roles_errors.PermissionDeniedError:
        detail = "Access denied for caller"
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=schema.responses.roles.errors.PermissionDeniedResponseBody.new(
                detail=detail
            ).model_dump(),
        )
    items = [
        schema.responses.roles.UserRoleItem(
            login=user.login,
            roles=user.roles,
        )
        for user in users
    ]
    return schema.responses.roles.GetUsersResponseBody.create(users=items)


@roles_router.post(
    "/roles",
    status_code=status.HTTP_200_OK,
    response_model=schema.responses.roles.SetRolesResponseBody,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": schema.responses.roles.errors.CannotModifyAdminResponseBody
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": schema.responses.roles.errors.UnauthorizedResponseBody
        },
        status.HTTP_403_FORBIDDEN: {
            "model": schema.responses.roles.errors.PermissionDeniedResponseBody
        },
        status.HTTP_404_NOT_FOUND: {
            "model": schema.responses.roles.errors.UserNotFoundResponseBody
        },
    },
)
async def set_roles(
    token: Annotated[str, Header()],
    body: schema.requests.roles.SetRolesRequestBody,
) -> schema.responses.roles.SetRolesResponseBody | JSONResponse:
    try:
        user = await dependency.manage_roles.set_roles(
            token=token,
            target_login=body.target_login,
            roles=body.roles,
        )
    except roles_errors.UnauthorizedError:
        detail = "Unauthorized"
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=schema.responses.roles.errors.UnauthorizedResponseBody.new(
                detail=detail
            ).model_dump(),
        )
    except roles_errors.PermissionDeniedError:
        detail = "Permission denied for caller"
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=schema.responses.roles.errors.PermissionDeniedResponseBody.new(
                detail=detail
            ).model_dump(),
        )
    except roles_errors.UserNotFoundError:
        detail = "Target user not found"
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=schema.responses.roles.errors.UserNotFoundResponseBody.new(
                detail=detail
            ).model_dump(),
        )
    except roles_errors.CannotModifyAdminError:
        detail = "Cannot modify admin roles"
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=schema.responses.roles.errors.CannotModifyAdminResponseBody.new(
                detail=detail
            ).model_dump(),
        )
    message = "Roles updated"
    return schema.responses.roles.SetRolesResponseBody.create(
        message=message,
        login=user.login,
        roles=user.roles,
    )
