from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="пост", callback_data="post_to_channel"),
            KeyboardButton(text="удалить", callback_data="delete"),
        ],
        [
            KeyboardButton(text="заблокировать", callback_data="ban_user"),
        ],
    ],
    resize_keyboard=True,
)
