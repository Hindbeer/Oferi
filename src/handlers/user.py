from aiogram import Bot, F, Router

# from aiogram.enums import InputMediaType
# from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.utils.markdown import code, text

import config
from keyboards.admin_keyboards import admin_keyboard
from midlewares.media_group_midleware import MediaGroupMidleware
from utils.media_utils import MediaUtils

router = Router()
router.message.middleware(MediaGroupMidleware())
bot = Bot(config.BOT_TOKEN)
media_utils = MediaUtils(bot)


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        "Добро пожаловать! Кидайте сюда свои смешные приколы и анекдоты. Ваши приколы оценят админы и запостят в телеграм канал"
    )


@router.message(F.photo | F.video)
async def forward_media(message: Message) -> None:
    caption = text(
        text(message.caption if message.caption is not None else ""),
        text(
            code(f"👤 {message.from_user.full_name}"),
        ),
        sep="\n\n",
    )

    await media_utils.send_media(
        message=message,
        caption=caption,
        reply_markup=admin_keyboard,
    )

    await message.answer("Сообщение было отправлено!")


@router.message(~F.text.startswith("/"))
async def forward_text(message: Message) -> None:
    caption = text(
        text(message.text if message.text is not None else ""),
        text(
            code(f"👤 {message.from_user.full_name}"),
        ),
        sep="\n\n",
    )

    await bot.send_message(
        chat_id=config.ADMIN_ID,
        text=caption,
        reply_markup=admin_keyboard,
        parse_mode=ParseMode.MARKDOWN_V2,
    )

    await message.answer("Сообщение было отправлено!")


#
# FIX: поправить этот кусок, чтобы можно было переслать группу медиа
#
# @router.message(F.photo | F.video)
# async def handle_media_group(
#     message: Message, media_group: list[Message] | None = None
# ) -> None:
#     if not media_group:
#         await bot.send_photo(
#             chat_id=config.ADMIN_ID,
#             photo=get_media_id(message),
#             caption=message.caption,
#         )
#         return
#
#     builder = MediaGroupBuilder()
#     for message in media_group:
#         builder.add(
#             type=InputMediaType.VIDEO if message.video else InputMediaType.PHOTO,
#             media=get_media_id(message),
#             caption=message.caption,
#             caption_entities=message.caption_entities,
#             has_spoiler=message.has_media_spoiler,
#             parse_mode=None,
#         )
#
#     media = builder.build()
#
#     await bot.send_media_group(
#         chat_id=config.ADMIN_ID,
#         media=media,
#     )
#
