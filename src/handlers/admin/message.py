from aiogram import Bot, F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.media_group import MediaGroupBuilder

from config import settings
from keyboards import admin_keyboards
from models import Post
from utils import CaptionUtils, ViewPostsState
from filters import Admin

router = Router()
bot = Bot(settings.BOT_TOKEN)


@router.message(F.text.lower() == "🗂 посты", Admin())
async def view_posts(message: Message, state: FSMContext) -> None:
    await state.set_state(ViewPostsState.choose_view_type)

    pending_posts = await Post.find_all().to_list()

    if not pending_posts:
        await message.answer("Новых постов нет")
        await state.set_state(ViewPostsState.choose_view_type)
        await message.answer(
            "Выберите опцию:", reply_markup=admin_keyboards.admin_menu_keyboard
        )
        return None

    await message.answer("Переходим в меню постов.", reply_markup=ReplyKeyboardRemove())
    await message.answer(
        "Посты:",
        reply_markup=admin_keyboards.admin_post_keyboard,
    )

    post_ids = [post.id for post in pending_posts]
    await state.update_data(pending_post_ids=post_ids, current_post_index=0)
    await state.set_state(ViewPostsState.viewing_pending_posts)

    await show_next_post(message, state, bot)


async def show_next_post(message: Message, state: FSMContext, bot: Bot) -> None:
    data = await state.get_data()
    pending_post_ids: list[int] = data.get("pending_post_ids", [])
    current_index: int = data.get("current_post_index", 0)

    if not pending_post_ids or current_index >= len(pending_post_ids):
        await message.answer(
            "Вы посмотрели все посты.",
            reply_markup=admin_keyboards.admin_menu_keyboard,
        )
        await state.set_state(ViewPostsState.choose_view_type)
        return None

    post_ids_to_show = pending_post_ids[current_index]

    post_data = await Post.find_one(Post.id == post_ids_to_show)

    if post_data:
        text = CaptionUtils.build_caption(
            text=post_data.caption, user_full_name=post_data.user_full_name
        )
        if post_data.media is not None:
            builder = MediaGroupBuilder()

            for i, file in enumerate(post_data.media):
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
    else:
        await message.answer("Не удалось найти пост. Пропускаем...")
        await state.update_data(current_post_index=current_index + 1)
        await show_next_post(message, state, bot)


@router.message(
    ViewPostsState.viewing_pending_posts, F.text.lower() == "✉️ пост", Admin()
)
async def send_post(message: Message, state: FSMContext, bot: Bot) -> None:
    data = await state.get_data()
    current_index = data.get("current_post_index")
    pending_post_ids: list[int] = data.get("pending_post_ids", [])
    post_ids_to_show = pending_post_ids[current_index]

    await state.update_data(current_post_index=current_index + 1)
    print(current_index, data, sep="\n")

    post_data = await Post.find_one(Post.id == post_ids_to_show)

    if post_data:
        text = CaptionUtils.build_caption(
            text=post_data.caption, user_full_name=post_data.user_full_name
        )
        if post_data.media is not None:
            builder = MediaGroupBuilder()
            for i, file in enumerate(post_data.media):
                builder.add(
                    type=file.type,
                    media=file.file_id,
                    caption=text if i == 0 else None,
                    parse_mode=ParseMode.HTML,
                )
            media_group = builder.build()
            await bot.send_media_group(
                chat_id=settings.TELEGRAM_CHANNEL_ID, media=media_group
            )
        else:
            await bot.send_message(chat_id=settings.TELEGRAM_CHANNEL_ID, text=text)

        await message.answer("Пост опубликован")

    await post_data.delete()

    await show_next_post(message, state, bot)


@router.message(
    ViewPostsState.viewing_pending_posts, F.text.lower() == "🗑 удалить", Admin()
)
async def delete_post(message: Message, state: FSMContext, bot: Bot) -> None:
    data = await state.get_data()
    current_index = data.get("current_post_index")
    pending_post_ids: list[int] = data.get("pending_post_ids", [])
    post_ids_to_show = pending_post_ids[current_index]

    await state.update_data(current_post_index=current_index + 1)
    print(current_index, data, sep="\n")

    await Post.find_one(Post.id == post_ids_to_show).delete()

    await message.answer("удален")

    await show_next_post(message, state, bot)


@router.message(
    ViewPostsState.viewing_pending_posts, F.text.lower() == "🚷 заблокировать", Admin()
)
async def ban_user(message: Message, state: FSMContext, bot: Bot) -> None:
    pass


@router.message(F.text.lower() == "🔙 главное меню", Admin())
async def back_to_main_menu(message: Message) -> None:
    await message.answer(
        "Главное меню:", reply_markup=admin_keyboards.admin_menu_keyboard
    )


@router.message(F.text.lower() == "⚙️ настройки", Admin())
async def settings_menu(message: Message) -> None:
    await message.answer(
        "Настройки:", reply_markup=admin_keyboards.admin_settings_menu_keyboard
    )


@router.message(F.text.lower() == "✅ разбанить", Admin())
async def unbun_menu(message: Message) -> None:
    await message.answer(
        "Введите id/username пользователя:",
        reply_markup=admin_keyboards.admin_settings_menu_keyboard,
    )
