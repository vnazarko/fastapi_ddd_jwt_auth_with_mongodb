# infrastructure/database/user_motor_repository.py
from abc import ABC
from typing import Optional, Mapping

from icecream import ic
from pydantic import EmailStr

from src.core.config import settings
from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


class UserMotorRepository(UserRepository, ABC):
    def __init__(self, db_client: AsyncIOMotorClient, db_name: str = "test"):
        self.db = db_client[db_name]
        self.collection = self.db.get_collection(settings.db.users_collection)

    async def find_by_email(self, email: EmailStr) -> Optional[User]:
        user_data = await self.collection.find_one({"email": email})
        if user_data:
            return self._document_to_user(user_data)
        return None

    async def find_by_id(self, id: int) -> Optional[User]:
        user_data = await self.collection.find_one({"id": id})
        if user_data:
            return self._document_to_user(user_data)
        return None

    async def get_last_id(self) -> int:
        last_user = await self.collection.find().sort({'_id':-1}).limit(1).to_list()
        if len(last_user) > 0:
           return self._document_to_user(last_user[0]).id
        return 0

    async def save(self, user_data: User) -> None:
        await self.collection.insert_one(user_data.to_dict())

    def _document_to_user(self, user_data) -> User:
        return User(
            id=user_data['id'],
            email=user_data['email'],
            hashed_password=user_data['hashed_password'],
            is_active=user_data['is_active']
        )
