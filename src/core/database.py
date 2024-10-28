from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings

client = AsyncIOMotorClient(settings.db.url)
database = client['test']
collection = database.get_collection(settings.db.users_collection)