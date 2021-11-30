#!/bin/sh
pipenv run python /emwiki/emwiki/manage.py build_graph
pipenv run python /emwiki/emwiki/manage.py load_articles
pipenv run python /emwiki/emwiki/manage.py load_symbols
