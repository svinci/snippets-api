from src.components.users.users_model import User
from src.components.users.repository import UsersRepository, USERS_REPOSITORY_NAME
from src.infrastructure.model import APIError
from src.infrastructure.crypto.hash import hash_password
from src.infrastructure.crypto.jwt import encode_jwt, decode_jwt

from beenchee.peanut import peanut
from uuid import uuid4
import logging, datetime

USERS_SERVICE_NAME = 'users_service'
logger = logging.getLogger(__name__)


@peanut(
    name=USERS_SERVICE_NAME,
    deps={
        'users_repository': USERS_REPOSITORY_NAME,
    },
    configs={
        'private_key_path': 'jwt.private_key_path',
        'public_key_path': 'jwt.public_key_path',
        'key_pass': 'jwt.key_pass',
        'algorithm': 'jwt.algorithm',
    }
)
class UsersService:
    private_key_path: str
    public_key_path: str
    key_pass: str
    algorithm: str
    
    users_repository: UsersRepository

    def get_all(self) -> list[User]:
        return self.users_repository.get_all()
    
    def get_by_id(self, user_id: str) -> User | None:
        return self.users_repository.get_by_id(user_id)

    def get_by_name(self, name: str) -> User | None:
        all_users = self.get_all()
        for user in all_users:
            if user.name == name:
                return user
        return None

    def create(self, name: str, password: str) -> User:
        user_id = uuid4().__str__()
        hashed_password, salt = hash_password(password)

        new_user = User(
            id=user_id,
            name=name,
            password_hash=hashed_password,
            password_salt=salt
        )
        self.users_repository.create(new_user)

        return new_user

    def get_token(self, name: str, password: str) -> tuple[User, str]:
        user = self.get_by_name(name)
        if user is None:
            raise APIError('Unauthorized', 401)

        hashed_password, _ = hash_password(password, user.password_salt)
        if user.password_hash != hashed_password:
            raise APIError('Unauthorized', 401)

        token_payload = {
            'user_id': user.id,
            'user_name': user.name,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        return user, encode_jwt(token_payload, self.private_key_path, self.key_pass, self.algorithm)

    def validate_token(self, token: str) -> User:
        claims = decode_jwt(token, self.public_key_path, self.algorithm)
        user_id = claims.get('user_id', None)
        if user_id is None:
            raise APIError('Unauthorized', 401)
        
        user = self.get_by_id(user_id)
        if user is None:
            raise APIError('Unauthorized', 401)
        
        return user
