from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


admin_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="пост", callback_data="post_to_channel"),
            InlineKeyboardButton(text="удалить", callback_data="delete"),
        ],
        [
            InlineKeyboardButton(text="заблокировать", callback_data="ban_user"),
        ],
    ]
)
