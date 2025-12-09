from aiogram import Bot, F, Router
from aiogram.enums import ParseMode

from aiogram.enums import InputMediaType
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.filters import CommandStart
from aiogram.types import Message, InputMediaPhoto, InputMediaVideo
from aiogram.utils.markdown import code, text

import config
from keyboards.admin_keyboards import admin_keyboard
from utils.media_utils import MediaUtils

router = Router()
bot = Bot(config.BOT_TOKEN)
media_utils = MediaUtils(bot)


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        "Добро пожаловать! Кидайте сюда свои смешные приколы и анекдоты. Ваши приколы оценят админы и запостят в телеграм канал"
    )


# @router.message(F.photo | F.video)
# async def forward_media(message: Message) -> None:
#     caption = text(
#         text(message.caption if message.caption is not None else ""),
#         text(
#             code(f"👤 {message.from_user.full_name}"),
#         ),
#         sep="\n\n",
#     )

#     await media_utils.send_media(
#         message=message,
#         caption=caption,
#         reply_markup=admin_keyboard,
#     )

#     await message.answer("Сообщение было отправлено!")


@router.message(~F.text.startswith("/"), ~F.photo, ~F.video)
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


@router.message()
async def forward_media_group(message: Message, album: list[Message]):
    media_group = []
    for media_message in album:
        # Обработка фото
        if media_message.photo:
            media_group.append(
                InputMediaPhoto(
                    media=media_message.photo[-1].file_id, caption=media_message.caption
                )
            )

        # Обработка видео
        elif media_message.video:
            media_group.append(
                InputMediaVideo(
                    media=media_message.video.file_id, caption=media_message.caption
                )
            )

    await message.answer_media_group(media_group)
    await message.answer("Сообщение было отправлено!")
