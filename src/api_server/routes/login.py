from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from api_server import schema
from api_server.app import dependency
from lisichki.domain.usecases.login import login_errors

login_router = APIRouter(
    prefix="/api",
    tags=["login"],
)


@login_router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=schema.responses.login.LoginResponseBody,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": schema.responses.login.errors.UserNotFoundResponseBody
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": schema.responses.login.errors.InvalidPasswordResponseBody
        },
    },
)
async def login(
    body: schema.requests.login.LoginRequestBody,
) -> schema.responses.login.LoginResponseBody | JSONResponse:
    try:
        user = await dependency.login_user.login(
            login=body.login,
            password=body.password,
        )
    except login_errors.UserNotFoundError:
        detail = "User not found"
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=schema.responses.login.errors.UserNotFoundResponseBody.new(
                detail=detail
            ).model_dump(),
        )
    except login_errors.InvalidPasswordError:
        detail = "Invalid password"
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=schema.responses.login.errors.InvalidPasswordResponseBody.new(
                detail=detail
            ).model_dump(),
        )
    message = "User logged in"
    return schema.responses.login.LoginResponseBody.create(
        message=message,
        access_token=user.token,
        login=user.login,
        roles=[role.value for role in user.roles],
    )
