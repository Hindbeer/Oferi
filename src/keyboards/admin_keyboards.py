from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


admin_post_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="✉️ пост", callback_data="post_to_channel"),
            KeyboardButton(text="🗑 удалить", callback_data="delete"),
        ],
        [
            KeyboardButton(text="🚷 заблокировать", callback_data="ban_user"),
            KeyboardButton(text="🔙 главное меню", callback_data="back_admin_menu"),
        ],
    ],
    resize_keyboard=True,
)

admin_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🗂 посты", callback_data="posts"),
            KeyboardButton(text="⚙️ настройки", callback_data="admin_settings"),
        ],
    ],
    resize_keyboard=True,
)

admin_settings_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="✅ разбанить", callback_data="unbun_menu"),
            KeyboardButton(text="🔙 главное меню", callback_data="back_admin_menu"),
        ],
    ],
    resize_keyboard=True,
)
