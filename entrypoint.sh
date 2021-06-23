#!/bin/sh
pipenv run python /emwiki/emwiki/manage.py migrate
pipenv run uwsgi /emwiki/uwsgi.ini
