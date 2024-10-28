import asyncio

from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from icecream import ic

from src.core.dependencies import auth_service
from src.domain.entities.user import User
from src.infrastructure.database.user_motor_repository import UserMotorRepository
from src.core.database import database, client
from src.core.http import oauth2_scheme

from src.presentation.api.auth import router as auth_router

app = FastAPI(title='FastAPI DDD Auth with MongoDB')

app.include_router(
    auth_router,
    prefix='/auth',
    tags=['Auth'],
)

@app.get('/test')
async def test(user: User = Depends(auth_service.get_user_from_access)):
    return user
