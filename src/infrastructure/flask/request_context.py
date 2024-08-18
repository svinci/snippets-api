from src.components.users import User
from src.infrastructure.model import APIError
from beenchee.peanut import peanut
from flask import g

REQUEST_CONTEXT_NAME = 'request_context'

@peanut(
    name = REQUEST_CONTEXT_NAME
)
class RequestContext:

    def set_user(self, user: User) -> None:
        self._set_request_context('user', user)

    def get_user(self) -> User | None:
        user = self._get_request_context('user')
        
        if user is None:
            raise APIError('No user in request context', 500)
        return user

    def clear_user(self) -> None:
        self._clear_request_context('user')

    def _set_request_context(self, key: str, value: any) -> None:
        if not hasattr(g, 'request_context'):
            g.request_context = {}

        g.request_context[key] = value

    def _get_request_context(self, key: str) -> any | None:
        if not hasattr(g, 'request_context'):
            g.request_context = {}

        return g.request_context.get(key, None)

    def _clear_request_context(self, key: str) -> None:
        if hasattr(g, 'request_context'):
            g.request_context.pop(key)
