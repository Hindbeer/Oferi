from aiogram.filters import BaseFilter
from aiogram.types import Message

from config import settings


class Admin(BaseFilter):
    async def __call__(
        self,
        message: Message,
    ) -> bool:
        if message.from_user.id == settings.ADMIN_ID:
            return True
        return False
