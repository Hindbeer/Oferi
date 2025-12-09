import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import settings
from handlers.user import message
from midlewares.album_midleware import AlbumMiddleware

dp = Dispatcher()


async def main() -> None:
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.MARKDOWN_V2,
            disable_notification=True,
            link_preview_is_disabled=True,
        ),
    )

    dp.include_routers(message.router)
    dp.message.middleware(AlbumMiddleware())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
