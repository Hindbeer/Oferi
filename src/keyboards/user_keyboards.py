from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


user_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⚙️ аноним", callback_data="user_settings"),
            KeyboardButton(text="💡 О боте", callback_data="bio"),
        ],
    ],
    resize_keyboard=True,
)
