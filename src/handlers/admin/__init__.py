__all__ = ("router",)

from aiogram import Router
from .message import router as message_router

router = Router()
router.include_routers(message_router)
