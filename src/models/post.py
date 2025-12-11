from beanie import Document
from pydantic import BaseModel


class File(BaseModel):
    type: str
    file_id: str


class Post(Document):
    user_id: int
    user_full_name: str
    caption: str | None
    media: list[File] | None

    class Settings:
        name: str = "posts"
