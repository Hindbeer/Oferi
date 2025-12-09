from aiogram import Bot
from aiogram.types import Message, ReplyMarkupUnion
from aiogram.enums import ParseMode

from config import settings


class MediaUtils:
    def __init__(self, bot: Bot):
        self.bot = bot

    def get_media_id(self, message: Message) -> str:
        return message.video and message.video.file_id or message.photo[-1].file_id

    async def send_media(
        self, message: Message, caption: str, reply_markup: ReplyMarkupUnion
    ) -> None:
        if message.photo:
            await self.bot.send_photo(
                chat_id=settings.ADMIN_ID,
                photo=self.get_media_id(message),
                caption=caption,
                parse_mode=ParseMode.HTML,
            )
        elif message.video:
            await self.bot.send_video(
                chat_id=settings.ADMIN_ID,
                video=self.get_media_id(message),
                caption=caption,
                parse_mode=ParseMode.HTML,
            )
