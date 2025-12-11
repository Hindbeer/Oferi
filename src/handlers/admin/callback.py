from aiogram import Bot, F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.media_group import MediaGroupBuilder

from keyboards import admin_keyboards
from models import Post
from utils import CaptionUtils, ViewPostsState

router = Router()


@router.callback_query(F.data == "post_to_channel")
async def post_to_channel(callback: CallbackQuery) -> None:
    await callback.answer(
        "Пост успешно отправлен",
    )


@router.callback_query(F.data == "delete")
async def delete(callback: CallbackQuery) -> None:
    await callback.answer("Пост был удален")
    await callback.message.delete()


@router.callback_query(ViewPostsState.choose_view_type, F.data == "posts")
async def process_view_who_liked_me(
    callback_query: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    print(1)

    pending_posts = await Post.find_all().to_list()

    if not pending_posts:
        await callback_query.message.answer("Новых постов нет")
        await state.set_state(ViewPostsState.choose_view_type)
        await callback_query.message.answer(
            "Выберите опцию:", reply_markup=admin_keyboards.admin_menu_keyboard()
        )
        return None

    post_ids = [post.id for post in pending_posts]
    await state.update_data(pending_post_ids=post_ids, current_post_index=0)
    await state.set_state(ViewPostsState.viewing_pending_posts)

    await show_next_post(callback_query.message, state, bot)


async def show_next_post(message: Message, state: FSMContext, bot: Bot) -> None:
    data = await state.get_data()
    pending_post_ids: list[int] = data.get("pending_post_ids", [])
    current_index: int = data.get("current_pending_index", 0)

    if not pending_post_ids or current_index >= len(pending_post_ids):
        await message.answer(
            "Вы все посты.",
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
            await message.answer(reply_markup=admin_keyboards.admin_post_keyboard)
        else:
            await message.answer(text)
            await message.answer(reply_markup=admin_keyboards.admin_post_keyboard)

        await state.update_data(current_post_index=current_index + 1)
        await show_next_post(message, state, bot)

    else:
        await message.answer("Не удалось найти пост. Пропускаем...")
        await state.update_data(current_pending_index=current_index + 1)
        await show_next_post(message, state, bot)
