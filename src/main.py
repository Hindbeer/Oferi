import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import settings
from handlers import router as main_router
from midlewares.album_midleware import AlbumMiddleware

from utils import db

dp = Dispatcher()


async def main() -> None:
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            disable_notification=True,
            link_preview_is_disabled=True,
        ),
    )

    await db.init()

    dp.include_routers(main_router)
    dp.message.middleware(AlbumMiddleware())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
