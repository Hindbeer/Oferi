import asyncio
from collections import defaultdict
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message

DataType = dict[str, Any]
GroupMessages = list[Message]


class MediaGroupMidleware(BaseMiddleware):
    def __init__(self, timeout: float = 0.3):
        self.timeout = timeout
        self.group_messages = defaultdict[str, GroupMessages](list)

    def get_count(self, message: Message) -> int:
        return len(self.group_messages[message.media_group_id])

    def store_media_group_message(self, message: Message) -> int:
        self.group_messages[message.media_group_id].append(message)
        return self.get_count(message)

    def get_result_group(self, message: Message) -> GroupMessages:
        group_messages = self.group_messages.pop(message.media_group_id)
        group_messages.sort(key=lambda m: m.message_id)
        return group_messages

    async def __call__[T](
        self,
        handler: Callable[[Message, DataType], Awaitable[T]],
        event: Message,
        data: DataType,
    ) -> T | None:
        if event.media_group_id is None:
            return await handler(event, data)

        count = self.store_media_group_message(event)
        await asyncio.sleep(self.timeout)

        new_count = self.get_count(event)
        if new_count != count:
            return None

        data.update(group_messages=self.get_result_group(event))

        return await handler(event, data)
