from pydantic import BaseModel, Field, StrictStr


class RegistrationRequestBody(BaseModel):
    login: StrictStr = Field(
        description="User login",
        examples=["Alfredo"],
    )
    password: StrictStr = Field(
        description="User password",
        examples=["StrongPassword123!"],
    )
