from aiogram import Bot, F, Router
from aiogram.enums import InputMediaType
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import settings
from models import Post
from type import File

router = Router()
bot = Bot(settings.BOT_TOKEN)


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        "Добро пожаловать! Кидайте сюда свои смешные приколы и анекдоты. Ваши приколы оценят админы и запостят в телеграм канал"
    )
    print(message)


@router.message(~F.text.startswith("/"), ~F.photo, ~F.video)
async def forward_text(message: Message) -> None:
    post: Post = Post(
        user_id=message.from_user.id,
        user_full_name=message.from_user.full_name,
        caption=message.text,
        media=None,
    )

    await post.insert()

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

    files: list[File] = []
    text: str

    if not album:
        """Если фото/видео одно"""
        files.append(
            File(
                type=InputMediaType.VIDEO if message.video else InputMediaType.PHOTO,
                file_id=message.video.file_id
                if message.video
                else message.photo[-1].file_id,
            )
        )

        text = message.caption

    else:
        """Если группа медиа"""
        for i, media_message in enumerate(album):
            files.append(
                File(
                    type=InputMediaType.VIDEO
                    if media_message.video
                    else InputMediaType.PHOTO,
                    file_id=media_message.video.file_id
                    if media_message.video
                    else media_message.photo[-1].file_id,
                )
            )
            text = media_message.caption if i == 0 else text

    post = Post(
        user_id=message.from_user.id,
        user_full_name=message.from_user.full_name,
        caption=text,
        media=files,
    )

    await post.insert()
    await message.answer("Сообщение было отправлено!")
