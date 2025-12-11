from beanie import Document

from type import File


class Post(Document):
    user_id: int
    user_full_name: str
    caption: str | None
    media: list[File] | None

    class Settings:
        name: str = "posts"
