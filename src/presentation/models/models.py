from abc import ABC

from pydantic import BaseModel


class SuccessfulResponse(BaseModel):
    payload: str | dict
    status: str = 'ok'
