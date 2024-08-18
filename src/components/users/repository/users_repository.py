from src.components.users.users_model import User

from abc import ABC, abstractmethod

USERS_REPOSITORY_NAME='users_repository'


class UsersRepository(ABC):

    @abstractmethod
    def get_all(self) -> list[User]:
        pass

    @abstractmethod
    def get_by_id(self, user_id: str) -> User | None:
        pass

    @abstractmethod
    def create(self, user: User) -> None:
        pass
