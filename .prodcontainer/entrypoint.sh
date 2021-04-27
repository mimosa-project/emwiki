#!/bin/sh

pipenv sync
pipenv run python /workspace/emwiki/emwiki/manage.py migrate
pipenv run python /workspace/emwiki/emwiki/manage.py register_db all
exec "$@"