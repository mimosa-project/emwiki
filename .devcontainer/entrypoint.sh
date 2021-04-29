#!/bin/sh

python /workspace/emwiki/manage.py makemigrations
python /workspace/emwiki/manage.py migrate
python /workspace/emwiki/manage.py build_htmlizedmml
python /workspace/emwiki/manage.py build_mmlreference
python /workspace/emwiki/manage.py build_search_data
python /workspace/emwiki/manage.py load_articles
python /workspace/emwiki/manage.py load_symbols

exec "$@"