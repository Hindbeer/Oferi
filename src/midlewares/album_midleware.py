import asyncio
from typing import Any, Awaitable, Callable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message

DataType = dict[str, Any]
GroupMessages = list[Message]


class AlbumMiddleware(BaseMiddleware):
    """
    Waiting for all pictures in media group will be uploaded
    """

    album_data: dict = {}

    def __init__(self, latency: Union[int, float] = 0.6):
        self.latency = latency

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        message: Message,
        data: dict[str, Any],
    ) -> Any:
        if not message.media_group_id:
            await handler(message, data)
            return
        try:
            self.album_data[message.media_group_id].append(message)
        except KeyError:
            self.album_data[message.media_group_id] = [message]
            await asyncio.sleep(self.latency)

            data["_is_last"] = True
            data["album"] = self.album_data[message.media_group_id]
            await handler(message, data)

        if message.media_group_id and data.get("_is_last"):
            del self.album_data[message.media_group_id]
            del data["_is_last"]
