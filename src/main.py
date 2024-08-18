from src.app import App, APP_NAME

from beenchee.peanut import get_peanut
from flask import Flask
import logging

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - [%(levelname)s] [%(process)d:%(threadName)s] (%(module)s:%(lineno)d) %(message)s'
)

module: App = get_peanut(APP_NAME)
flask_app: Flask = module.run()
