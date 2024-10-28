from typing import Optional

from fastapi.security import HTTPAuthorizationCredentials
from pydantic import EmailStr

from src.core.http import oauth2_scheme, http_bearer
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.enums.token import JWTTypes
from src.infrastructure.security.password_hasher import PasswordHasher
from src.infrastructure.security.jwt_handler import JWTHandler
from src.domain.entities.user import User
from fastapi import HTTPException, status, Depends


class AuthService:
    def __init__(self, user_repo: UserRepository, password_hasher: PasswordHasher, jwt_handler: JWTHandler):
        self.user_repo = user_repo
        self.password_hasher = password_hasher
        self.jwt_handler = jwt_handler

    async def register(self, email: EmailStr, password: str) -> None:
        existing_user = await self.user_repo.find_by_email(email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email is already taken"
            )

        hashed_password = self.password_hasher.hash(password)
        id = await self.user_repo.get_last_id() + 1

        new_user = User(id=id, email=email, hashed_password=hashed_password)

        await self.user_repo.save(new_user)

    async def auth_user(self, email: EmailStr, password: str) -> tuple[str, str]:
        existing_user = await self.user_repo.find_by_email(email)

        if existing_user and self.password_hasher.verify(password, existing_user.hashed_password):
            if self.verify_user_permissions(existing_user):
                jwt_payload = {
                    'sub': existing_user.id
                }
                return self.jwt_handler.create_tokens(jwt_payload)

    async def get_user_from_access(self, token: str = Depends(oauth2_scheme)) -> User:
        return await self._get_user_from_token_of_type(JWTTypes.ACCESS, token=token)

    async def get_user_from_refresh(self, credentials: HTTPAuthorizationCredentials = Depends(http_bearer)) -> User:
        return await self._get_user_from_token_of_type(JWTTypes.REFRESH, token=credentials.credentials)

    async def _get_user_from_token_of_type(self, token_type: JWTTypes, token: str) -> User:
        token_payload = self.jwt_handler.verify_token(token)

        self.jwt_handler.validate_token_type(token_payload, token_type.value)

        user_id = token_payload.get("sub")
        user = await self.user_repo.find_by_id(user_id)
        if user and self.verify_user_permissions(user):
            return user
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not exist or he is inactive"
        )


    def verify_user_permissions(self, user: User):
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not active"
            )
        return True
