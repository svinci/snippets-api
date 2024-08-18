from src.components.users.repository.users_repository import UsersRepository, USERS_REPOSITORY_NAME
from src.components.users.users_model import User
from src.infrastructure.storage.csv_repository import CSVRepository
from src.infrastructure.dataclasses import from_dict, to_dict
from beenchee.peanut import peanut


@peanut(
    name=USERS_REPOSITORY_NAME,
    configs={
        'storage_folder': 'storage_folder'
    }
)
class UsersCSVRepository(UsersRepository):
    storage_folder: str
    csv_repository: CSVRepository

    def post_construct(self):
        self.csv_repository = CSVRepository(self.storage_folder, 'users.csv')
    
    def get_all(self) -> list[User]:
        all_rows = self.csv_repository.read()
        return [from_dict(User, row) for row in all_rows]

    def get_by_id(self, user_id: str) -> User | None:
        all_users = self.get_all()

        for user in all_users:
            if user.id == user_id:
                return user
        return None

    def create(self, user: User) -> None:
        new_row = to_dict(user)
        self.csv_repository.write([new_row])
