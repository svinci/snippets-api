from src.infrastructure.model import Router, APIError

from werkzeug.exceptions import HTTPException
from flask import Flask, request, Response
from beenchee.peanut import peanut
import logging

logger = logging.getLogger(__name__)

ERROR_HANDLER_NAME = 'error_handler'


@peanut(
    name=ERROR_HANDLER_NAME
)
class ErrorHandler(Router):

    def route(self, app: Flask):
        @app.errorhandler(Exception)
        def handle_exception(e):
            if isinstance(e, HTTPException):
                return e
            
            if isinstance(e, APIError):
                return { 'message': e.message }, e.code

            logger.error(f'Unhandled exception: {e}')
            return { 'message': 'Internal server error' }, 500
