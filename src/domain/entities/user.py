from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str | bytes
    is_active: bool = True

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'email': self.email,
            'hashed_password': self.hashed_password,
            'is_active': self.is_active,
        }
