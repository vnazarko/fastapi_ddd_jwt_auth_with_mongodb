from enum import Enum


class JWTTypes(Enum):
    ACCESS = 'access'
    REFRESH = 'refresh'