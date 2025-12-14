import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from fluent_compiler.bundle import FluentBundle
from fluentogram import FluentTranslator, TranslatorHub

from config import settings
from handlers import router as main_router
from midlewares import AlbumMiddleware, TranslateMiddleware
from utils import db

dp = Dispatcher()

t_hub = TranslatorHub(
    {
        "en": ("en", "ru"),
        "ru": ("ru",),
    },
    translators=[
        FluentTranslator(
            locale="ru",
            translator=FluentBundle.from_files(
                "ru-RU",
                filenames=[
                    "i18n/ru/text.ftl",
                    "i18n/ru/button.ftl",
                ],
            ),
        ),
        FluentTranslator(
            locale="en",
            translator=FluentBundle.from_files(
                "en-US",
                filenames=[
                    "i18n/en/text.ftl",
                    "i18n/en/button.ftl",
                ],
            ),
        ),
    ],
    root_locale="en",
)


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
    dp.message.outer_middleware(TranslateMiddleware())
    dp.callback_query.outer_middleware(TranslateMiddleware())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
