from pydantic import BaseModel, Field, StrictStr


class SendMessageRequestBody(BaseModel):
    text: StrictStr = Field(
        description="Message text",
        examples=["Hello world!"],
    )
