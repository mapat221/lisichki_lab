from datetime import datetime

from pydantic import BaseModel, Field, StrictStr
from typing_extensions import Self


class MessageItem(BaseModel):
    id_: StrictStr = Field(
        description="Message id",
        examples=["1"],
    )
    author_login: StrictStr = Field(
        description="Author login",
        examples=["Alfredo"],
    )
    text: StrictStr = Field(
        description="Message text",
        examples=["Hello world!"],
    )
    created_at: datetime


class GetMessagesResponseBody(BaseModel):
    messages: list[MessageItem]

    @classmethod
    def create(cls, messages: list[MessageItem]) -> Self:
        return cls(messages=messages)


class SendMessageResponseBody(BaseModel):
    message: MessageItem

    @classmethod
    def create(cls, message: MessageItem) -> Self:
        return cls(message=message)


class DeleteMessageResponseBody(BaseModel):
    message: StrictStr = Field(
        description="Delete status", examples=["Message deleted"]
    )

    @classmethod
    def create(cls, message: str) -> Self:
        return cls(message=message)
