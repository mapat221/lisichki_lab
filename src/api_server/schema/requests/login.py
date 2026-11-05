from pydantic import BaseModel, Field, StrictStr


class LoginRequestBody(BaseModel):
    login: StrictStr = Field(
        description="User login",
        examples=["Alfredo"],
    )
    password: StrictStr = Field(
        description="User password",
        examples=["StrongPassword123!"],
    )
