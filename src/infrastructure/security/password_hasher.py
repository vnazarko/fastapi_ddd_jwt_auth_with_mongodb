from passlib.context import CryptContext


class PasswordHasher:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def hash(self, password: str) -> str | bytes:
        return self.pwd_context.hash(password)

    def verify(self, hashed_password: str | bytes, password: str) -> bool:
        return self.pwd_context.verify(hashed_password, password)