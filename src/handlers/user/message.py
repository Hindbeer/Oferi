from aiogram import Bot, F, Router
from aiogram.enums import InputMediaType, ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.media_group import MediaGroupBuilder

from config import settings

router = Router()
bot = Bot(settings.BOT_TOKEN)


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        "Добро пожаловать! Кидайте сюда свои смешные приколы и анекдоты. Ваши приколы оценят админы и запостят в телеграм канал"
    )
    print(message)


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


# ToDo: mb refactor
@router.message()
async def forward_media(
    message: Message,
    album: list[Message] | None = None,
) -> None:
    """
    Оптравка медиа, в том числе группы медиа
    """
    if message.video:
        await bot.send_video(
            chat_id=settings.ADMIN_ID,
            video=message.video.file_id,
            caption=build_caption(message),
            parse_mode=ParseMode.HTML,
        )
    else:
        await bot.send_photo(
            chat_id=settings.ADMIN_ID,
            photo=message.photo[-1].file_id,
            caption=build_caption(message),
            parse_mode=ParseMode.HTML,
        )

    """Если фото/видео одно"""
    if not album:
        return None

    """Если группа медиа"""
    builder = MediaGroupBuilder()

    for i, media_message in enumerate(album):
        builder.add(
            type=(
                InputMediaType.VIDEO if media_message.video else InputMediaType.PHOTO
            ),
            media=(
                media_message.video.file_id
                if media_message.video
                else media_message.photo[-1].file_id
            ),
            caption=build_caption(message) if i == 0 else media_message.caption,
            parse_mode=ParseMode.HTML,
        )

    media_group = builder.build()

    await bot.send_media_group(chat_id=settings.ADMIN_ID, media=media_group)
    await message.answer("Сообщение было отправлено!")
