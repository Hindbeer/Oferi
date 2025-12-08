from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.types import Message, ReplyMarkupUnion

import config


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
                chat_id=config.ADMIN_ID,
                photo=self.get_media_id(message),
                caption=caption,
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=reply_markup,
            )
        elif message.video:
            await self.bot.send_video(
                chat_id=config.ADMIN_ID,
                video=self.get_media_id(message),
                caption=caption,
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=reply_markup,
            )
