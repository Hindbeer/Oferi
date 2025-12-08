import config

from midlewares.media_group_midleware import MediaGroupMidleware

from aiogram import Bot, Router, F
from aiogram.enums import InputMediaType
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()
router.message.middleware(MediaGroupMidleware())
bot = Bot(config.BOT_TOKEN)


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Отправь что-то смешное! Админи будут смеяться :)")


def get_media_id(message: Message) -> str:
    return message.video and message.video.file_id or message.photo[-1].file_id


@router.message(F.photo | F.video)
async def handle_media_group(
    message: Message, media_group: list[Message] | None = None
):
    if not media_group:
        await bot.send_photo(
            chat_id=config.ADMIN_ID,
            photo=get_media_id(message),
            caption=message.caption,
        )
        return

    builder = MediaGroupBuilder()
    for message in media_group:
        builder.add(
            type=InputMediaType.VIDEO if message.video else InputMediaType.PHOTO,
            media=get_media_id(message),
            caption=message.caption,
            caption_entities=message.caption_entities,
            has_spoiler=message.has_media_spoiler,
            parse_mode=None,
        )

    media = builder.build()

    await bot.send_media_group(
        chat_id=config.ADMIN_ID,
        media=media,
    )
