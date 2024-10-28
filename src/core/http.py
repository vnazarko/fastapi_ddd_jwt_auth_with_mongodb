from fastapi.security import HTTPBearer, OAuth2PasswordBearer

http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
