from abc import ABC, abstractmethod

from pydantic import EmailStr

from src.domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    def find_by_email(self, email: EmailStr) -> User:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> User:
        pass

    @abstractmethod
    def get_last_id(self) -> int:
        pass

    @abstractmethod
    def save(self, user: User) -> None:
        pass
