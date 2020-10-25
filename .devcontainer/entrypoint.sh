#!/bin/sh

python /workspace/emwiki/manage.py makemigrations
python /workspace/emwiki/manage.py migrate
python /workspace/emwiki/manage.py generate all
python /workspace/emwiki/manage.py register all

exec "$@"