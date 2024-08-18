from src.components.users import USERS_SERVICE_NAME, UsersService, User
from src.infrastructure.model import APIError
from src.infrastructure.flask.request_context import RequestContext, REQUEST_CONTEXT_NAME
from flask import request, g
from functools import wraps
from beenchee.peanut import peanut, get_peanut

AUTH_HANDLER_NAME = 'auth_handler'


@peanut(
    name=AUTH_HANDLER_NAME,
    deps={
        'users_service': USERS_SERVICE_NAME,
        'request_context': REQUEST_CONTEXT_NAME,
    }
)
class AuthenticationContextHandler:
    users_service: UsersService
    request_context: RequestContext

    def authenticate_request(self) -> None:
        token = self._get_auth_token()
        if token is None:
            raise APIError('No authorization provided.', 400)
        
        user = self._verify_token(token)
        self.request_context.set_user(user)
    
    def clear_authentication(self) -> None:
        self.request_context.clear_user()
    
    def _verify_token(self, token: str) -> User:
        return self.users_service.validate_token(token)

    def _get_auth_token(self) -> str | None:
        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            return None
        
        split = auth_header.split(' ')
        if len(split) != 2:
            return None
        
        return split[1]


def authenticated(handler):
    auth_handler: AuthenticationContextHandler = get_peanut(AUTH_HANDLER_NAME)

    @wraps(handler)
    def decorated(*args, **kwargs):
        try:
            auth_handler.authenticate_request()
            return handler(*args, **kwargs)
        finally:
            auth_handler.clear_authentication()

    return decorated
