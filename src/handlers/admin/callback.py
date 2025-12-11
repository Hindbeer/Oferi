import config
from keyboards import admin_keyboards

from aiogram import Router, F
from aiogram.types import CallbackQuery

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
