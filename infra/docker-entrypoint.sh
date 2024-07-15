#!/bin/bash

poetry run task migrate
poetry run task collectstatic
poetry run task createsuperuser --noinput
poetry run task start 0:8000

exec "$@"
