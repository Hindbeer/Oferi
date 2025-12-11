from beanie import init_beanie
from pymongo import AsyncMongoClient

from models import Post


async def init() -> None:
    client = AsyncMongoClient("mongodb://localhost:27017")
    await init_beanie(database=client.db_name, document_models=[Post])
