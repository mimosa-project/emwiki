#!/bin/sh

pipenv sync
pipenv run python /workspace/emwiki/emwiki/manage.py migrate
python /workspace/emwiki/manage.py load_articles
python /workspace/emwiki/manage.py load_symbols

exec "$@"