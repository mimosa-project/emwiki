#!/bin/sh

python /workspace/emwiki/manage.py makemigrations
python /workspace/emwiki/manage.py migrate
python /workspace/emwiki/manage.py generate_files all
python /workspace/emwiki/manage.py register_db all

exec "$@"