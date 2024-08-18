from src.components.notes import NOTES_ROUTER_NAME
from src.components.users import USERS_ROUTER_NAME
from src.infrastructure.flask.request_logger import REQUEST_LOGGER_NAME
from src.infrastructure.flask.error_handler import ERROR_HANDLER_NAME
from src.infrastructure.model import Router

from peanut import peanut
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix


APP_NAME = 'app'

@peanut(
    name=APP_NAME,
    deps={
        'routers': [
            USERS_ROUTER_NAME,
            NOTES_ROUTER_NAME,
            REQUEST_LOGGER_NAME,
            ERROR_HANDLER_NAME,
        ],
    }
)
class App:
    routers: list[Router]

    def run(self) -> Flask:
        app = Flask(__name__)
        app.wsgi_app = ProxyFix(app.wsgi_app)

        for router in self.routers:
            router.route(app)
        
        return app
