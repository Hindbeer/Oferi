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


#
# class MediaGroupMidleware(BaseMiddleware):
#     def __init__(self, timeout: float = 0.3):
#         self.timeout = timeout
#         self.group_messages = defaultdict[str, GroupMessages](list)
#
#     def get_count(self, message: Message) -> int:
#         return len(self.group_messages[message.media_group_id])
#
#     def store_media_group_message(self, message: Message) -> int:
#         self.group_messages[message.media_group_id].append(message)
#         return self.get_count(message)
#
#     def get_result_group(self, message: Message) -> GroupMessages:
#         group_messages = self.group_messages.pop(message.media_group_id)
#         group_messages.sort(key=lambda m: m.message_id)
#         return group_messages
#
#     async def __call__[T](
#         self,
#         handler: Callable[[Message, DataType], Awaitable[T]],
#         event: Message,
#         data: DataType,
#     ) -> T | None:
#         if event.media_group_id is None:
#             return await handler(event, data)
#
#         count = self.store_media_group_message(event)
#         await asyncio.sleep(self.timeout)
#
#         new_count = self.get_count(event)
#         if new_count != count:
#             return None
#
#         data.update(group_messages=self.get_result_group(event))
#
#         return await handler(event, data)
#
