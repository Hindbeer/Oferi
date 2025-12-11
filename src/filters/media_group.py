from aiogram.filters import BaseFilter
from aiogram.types import Message


class MediaGroup(BaseFilter):
    async def __call__(
        self,
        message: Message,
        album: list[Message] | None = None,
    ) -> bool:
        if not album:
            return False
        return True
