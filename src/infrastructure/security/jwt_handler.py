import time
from datetime import datetime, timedelta
from typing import Optional, Tuple

from fastapi import HTTPException
import jwt
from jwt import DecodeError, ExpiredSignatureError
from starlette import status

from src.core.config import settings
from src.infrastructure.enums.token import JWTTypes


class JWTHandler:
    def __init__(self,
                 private_key: str = settings.jwt.private_key_path.read_text(),
                 public_key: str = settings.jwt.public_key_path.read_text(),
                 algorithm: str = settings.jwt.algorithm,
                 access_token_expire_minutes: int = settings.jwt.access_token_expire_minutes,
                 refresh_token_expire_days: int = settings.jwt.refresh_token_expire_days):
        self.private_key = private_key
        self.public_key = public_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days

    def create_tokens(self, token_data: dict):
        access_token = self._create_token(token_data, JWTTypes.ACCESS)
        refresh_token = self._create_token(token_data, JWTTypes.REFRESH,
                                           expire_timedelta=timedelta(days=self.refresh_token_expire_days))
        return access_token, refresh_token

    def verify_token(self, token: str | bytes) -> Optional[dict]:
        try:
            decoded_payload = self.decode_jwt(token)

            return decoded_payload
        except DecodeError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Invalid token, {e}')
        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Token expired')

    def validate_token_type(
            self,
            payload: dict,
            token_type: JWTTypes):
        if payload.get('type') == token_type:
            return True
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token type',
        )

    def decode_jwt(
            self,
            token: str | bytes,
            public_key: str = settings.jwt.public_key_path.read_text(),
            algorithm: str = settings.jwt.algorithm) -> dict:
        decoded = jwt.decode(
            jwt=token,
            key=public_key,
            algorithms=[algorithm]
        )

        return decoded

    def _create_token(self,
                      token_data: dict,
                      token_type: JWTTypes,
                      expire_minutes: int = settings.jwt.access_token_expire_minutes,
                      expire_timedelta: timedelta | None = None) -> str:
        jwt_payload = {'type': token_type.value}
        jwt_payload.update(token_data)

        return self._encode_jwt(
            payload=jwt_payload,
            expire_minutes=expire_minutes,
            expire_timedelta=expire_timedelta,
        )

    def _encode_jwt(
            self,
            payload: dict,
            private_key: str = settings.jwt.private_key_path.read_text(),
            algorithm: str = settings.jwt.algorithm,
            expire_minutes: int = settings.jwt.access_token_expire_minutes,
            expire_timedelta: timedelta | None = None,) -> str:
        to_encode = payload.copy()
        now = datetime.utcnow()
        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=expire_minutes)
        to_encode.update(
            exp=expire,
            iat=now,
        )

        encoded = jwt.encode(
            to_encode,
            private_key,
            algorithm=algorithm,
        )
        return encoded


