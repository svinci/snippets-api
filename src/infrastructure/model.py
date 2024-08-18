from abc import ABC, abstractmethod
from flask import Flask


class APIError(Exception):
    def __init__(self, message: str, code: int):
        self.message = message
        self.code = code

    def __str__(self):
        return f'HTTP Status {self.code}: {self.message}.'


ROUTERS_TAG = 'routers'


class Router(ABC):
    
    @abstractmethod
    def route(self, app: Flask) -> None:
        pass
