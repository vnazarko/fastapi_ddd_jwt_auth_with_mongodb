from fastapi import APIRouter, HTTPException, Depends, Form
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from icecream import ic
from pydantic import EmailStr
from starlette.requests import Request

from src.application.services.auth_service import AuthService
from src.core.database import collection
from src.core.http import http_bearer, oauth2_scheme
from src.domain.entities.user import User
from src.infrastructure.security.jwt_handler import JWTHandler
from src.presentation.models.auth import SuccessfulRegistration, TokenInfo
from src.presentation.schemas.auth import AuthSchema
from src.core.dependencies import get_auth_service, get_jwt_handler, auth_service
from src.core.config import settings

router = APIRouter(

)


@router.post("/register", response_model=SuccessfulRegistration)
async def register(user: AuthSchema, auth_service: AuthService = Depends(get_auth_service)):
    await auth_service.register(email=user.email, password=user.password)

    return SuccessfulRegistration()


@router.post("/login", response_model=TokenInfo)
async def login(username: EmailStr = Form(), password: str = Form(), auth_service: AuthService = Depends(get_auth_service)):
    access_token, refresh_token = await auth_service.auth_user(username, password)

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post("/refresh", response_model=TokenInfo, response_model_exclude_none=True)
async def refresh(user: User = Depends(auth_service.get_user_from_refresh),
                  jwt_handler: JWTHandler = Depends(get_jwt_handler)):
    access_token, refresh_token = jwt_handler.create_tokens({
        'sub': user.id
    })
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token
    )