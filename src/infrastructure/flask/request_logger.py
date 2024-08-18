from src.infrastructure.model import Router

from flask import Flask, request, Response
from beenchee.peanut import peanut
import logging

logger = logging.getLogger(__name__)

REQUEST_LOGGER_NAME = 'request_logger'


@peanut(
    name=REQUEST_LOGGER_NAME
)
class RequestLogger(Router):

    def route(self, app: Flask):
        @app.before_request
        def log_request():
            logger.info(f'Request: [{request.method}] {request.path}')

        @app.after_request
        def log_response(response: Response):
            logger.info(f'Response: [{request.method}] {request.path} {response.status_code}')
            return response
