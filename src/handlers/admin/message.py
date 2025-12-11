from aiogram import Bot, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.media_group import MediaGroupBuilder

from config import settings
from models import Post
from utils import CaptionUtils

router = Router()
bot = Bot(settings.BOT_TOKEN)


@router.message(Command("all"))
async def forward_text(message: Message) -> None:
    posts = await Post.find_all().to_list()

    for post in posts:
        text = CaptionUtils.build_caption(
            text=post.caption, user_full_name=post.user_full_name
        )
        if post.media is not None:
            builder = MediaGroupBuilder()

            for i, file in enumerate(post.media):
                builder.add(
                    type=file.type,
                    media=file.file_id,
                    caption=text if i == 0 else None,
                    parse_mode=ParseMode.HTML,
                )

            media_group = builder.build()

            await message.answer_media_group(media_group)
        else:
            await message.answer(text)
