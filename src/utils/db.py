from beanie import init_beanie
from pymongo import AsyncMongoClient

from config import settings
from models import Post


async def init() -> None:
    client = AsyncMongoClient(settings.HOST_URL)
    await init_beanie(database=client.db_name, document_models=[Post])
