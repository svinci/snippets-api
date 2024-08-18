from src.components.users.users_service import UsersService, USERS_SERVICE_NAME
from src.infrastructure.dataclasses import to_dict
from src.infrastructure.model import Router, ROUTERS_TAG

from beenchee.peanut import peanut
from flask import Flask, request

USERS_ROUTER_NAME='users_router'


@peanut(
    name=USERS_ROUTER_NAME,
    deps={
        'users_service': USERS_SERVICE_NAME,
    },
    tags=f'{ROUTERS_TAG}'
)
class UsersRouter(Router):
    users_service: UsersService

    def route(self, app: Flask) -> None:
        @app.route('/users', methods=['POST'])
        def create():
            name = request.json.get('name', '')
            password = request.json.get('password', '')

            user = self.users_service.create(
                name=name, 
                password=password
            )

            return to_dict(user)

        @app.route('/users/login', methods=['POST'])
        def login():
            name = request.json.get('name', '')
            password = request.json.get('password', '')

            user, token = self.users_service.get_token(name, password)

            return {
                'user': to_dict(user),
                'token': token
            }
