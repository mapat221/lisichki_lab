from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from api_server import schema
from api_server.app import dependency
from lisichki.domain.usecases.registration import registration_errors

registration_router = APIRouter(
    prefix="/api",
    tags=["registration"],
)


@registration_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=schema.responses.registration.RegistrationResponseBody,
    responses={
        status.HTTP_409_CONFLICT: {
            "model": schema.responses.registration.errors.UserAlreadyExistsResponseBody
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": schema.responses.registration.errors.InvalidLoginResponseBody
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": schema.responses.registration.errors.WeakPasswordResponseBody
        },
    },
)
async def register(
    body: schema.requests.registration.RegistrationRequestBody,
) -> schema.responses.registration.RegistrationResponseBody | JSONResponse:
    try:
        user = await dependency.registrate_user.registrate(
            login=body.login,
            password=body.password,
        )
    except registration_errors.UserAlreadyExistsError:
        detail = "User already exists"
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=schema.responses.registration.errors.UserAlreadyExistsResponseBody.new(
                detail=detail
            ).model_dump(),
        )
    except registration_errors.InvalidLoginError:
        detail = "User login is invalid"
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=schema.responses.registration.errors.InvalidLoginResponseBody.new(
                detail=detail
            ).model_dump(),
        )
    except registration_errors.WeakPasswordError:
        detail = "User password is so weak"
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=schema.responses.registration.errors.WeakPasswordResponseBody.new(
                detail=detail
            ).model_dump(),
        )
    message = "User registrated"
    return schema.responses.registration.RegistrationResponseBody.create(
        message=message,
        access_token=user.token,
        login=user.login,
        roles=[role.value for role in user.roles],
    )
