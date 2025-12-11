from aiogram import Bot, F, Router
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.utils.media_group import MediaGroupBuilder

from config import settings
from keyboards import admin_keyboards
from models import Post
from utils import CaptionUtils

router = Router()
bot = Bot(settings.BOT_TOKEN)


@router.message(F.text.lower() == "🗂 посты")
async def all_posts(message: Message) -> None:
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


@router.message(F.text.lower() == "🔙 главное меню")
async def back_to_main_menu(message: Message) -> None:
    await message.answer(
        "Главное меню:", reply_markup=admin_keyboards.admin_menu_keyboard
    )


@router.message(F.text.lower() == "⚙️ настройки")
async def settings_menu(message: Message) -> None:
    await message.answer(
        "Настройки:", reply_markup=admin_keyboards.admin_settings_menu_keyboard
    )


@router.message(F.text.lower() == "✅ разбанить")
async def unbun_menu(message: Message) -> None:
    await message.answer(
        "Введите id/username пользователя:",
        reply_markup=admin_keyboards.admin_settings_menu_keyboard,
    )
