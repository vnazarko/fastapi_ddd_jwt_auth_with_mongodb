from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from starlette import status

from src.application.services.auth_service import AuthService
from src.core.database import collection, client
from src.domain.entities.user import User
from src.infrastructure.database.user_motor_repository import UserMotorRepository
from src.infrastructure.security.jwt_handler import JWTHandler
from src.infrastructure.security.password_hasher import PasswordHasher

user_repo = UserMotorRepository(client)
password_hasher = PasswordHasher()
jwt_handler = JWTHandler()
auth_service = AuthService(user_repo, password_hasher, jwt_handler)

def get_auth_service() -> AuthService:
    return auth_service


def get_jwt_handler() -> JWTHandler:
    return jwt_handler


async def get_collection():
    yield collection

