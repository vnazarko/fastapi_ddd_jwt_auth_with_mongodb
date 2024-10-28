import os
from pathlib import Path

from pydantic import BaseModel, MongoDsn
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.parent.parent


class DatabaseConfig(BaseModel):
    url: MongoDsn = os.getenv('DB_URL')
    users_collection: str = os.getenv('USERS_COLLECTION')


class JWTConfig(BaseModel):
    private_key_path: Path = BASE_DIR / 'certs' / 'jwt-private.pem'
    public_key_path: Path = BASE_DIR / 'certs' / 'jwt-public.pem'
    algorithm: str = 'RS256'
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30


class Settings(BaseSettings):
    db: DatabaseConfig = DatabaseConfig()
    jwt: JWTConfig = JWTConfig()


settings = Settings()
