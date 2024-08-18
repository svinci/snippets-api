#!/usr/bin/env bash

pip3 install -r requirements.txt

PEANUT_CONFIG_FILE=./src/infrastructure/config/config.$1.json gunicorn -w ${2:-1} 'src.main:flask_app' --reload
