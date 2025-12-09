from aiogram import Bot, F, Router
from aiogram.filters import CommandStart
from aiogram.types import InputMediaPhoto, InputMediaVideo, Message
# from aiogram.utils.markdown import link, text

from aiogram.enums import ParseMode

from config import settings
from keyboards.admin_keyboards import admin_keyboard
from utils.media_utils import MediaUtils

router = Router()
bot = Bot(settings.BOT_TOKEN)
media_utils = MediaUtils(bot)


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        "Добро пожаловать! Кидайте сюда свои смешные приколы и анекдоты. Ваши приколы оценят админы и запостят в телеграм канал"
    )


def is_text_message(message: Message) -> bool:
    """
    Проверка сообщение на текстовое ли оно
    """
    return True if message.text else False


def escape_html(text: str) -> str:
    """
    Экранирование спецсимволов HTML
    """
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#x27;")
    )


def build_caption(message: Message) -> str:
    """
    Создание подписи под сообщением
    """
    original_caption = (
        message.text if is_text_message(message) else message.caption or ""
    )

    safe_caption = escape_html(original_caption)
    text_link = (
        f'<a href="{settings.BOT_LINK}">'
        f"👤 {escape_html(message.from_user.full_name)}"
        "</a>"
    )
    caption = f"{safe_caption}\n\n{text_link}"

    return caption


@router.message(~F.text.startswith("/"), ~F.photo, ~F.video)
async def forward_text(message: Message) -> None:
    await bot.send_message(
        chat_id=settings.ADMIN_ID,
        text=build_caption(message),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )
    await message.answer("Сообщение было отправлено!")


@router.message()
async def forward_media_group(
    message: Message,
    album: list[Message] | None = None,
) -> None:
    if album:
        media_group = []
        for i, media_message in enumerate(album):
            # Обработка фото
            if media_message.photo:
                media_group.append(
                    InputMediaPhoto(
                        media=media_message.photo[-1].file_id,
                        caption=(
                            build_caption(message) if i == 0 else media_message.caption
                        ),
                        parse_mode=ParseMode.HTML,
                    )
                )

            # Обработка видео
            elif media_message.video:
                media_group.append(
                    InputMediaVideo(
                        media=media_message.video.file_id,
                        caption=(
                            build_caption(message) if i == 0 else media_message.caption
                        ),
                        parse_mode=ParseMode.HTML,
                    )
                )

        await bot.send_media_group(chat_id=settings.ADMIN_ID, media=media_group)
        await message.answer("Сообщение было отправлено!")
    else:
        # Медиа одно
        await media_utils.send_media(message=message, caption=build_caption(message))
        await message.answer("Сообщение было отправлено!")
