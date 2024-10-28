from pydantic import BaseModel

from src.presentation.models.models import SuccessfulResponse


class SuccessfulRegistration(SuccessfulResponse):
    payload: str = 'User registered successfully'


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    type: str = 'Bearer'
