from aiogram.enums import InputMediaType
from pydantic import BaseModel


class File(BaseModel):
    type: InputMediaType
    file_id: str
