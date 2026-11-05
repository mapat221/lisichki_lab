from datetime import datetime

from pydantic import BaseModel


class Message(BaseModel):
    id_: str
    author_login: str
    text: str
    created_at: datetime
