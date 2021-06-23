#!/bin/sh
pipenv run python /emwiki/emwiki/manage.py build_htmlizedmml
pipenv run python /emwiki/emwiki/manage.py build_fmbibs
pipenv run python /emwiki/emwiki/manage.py build_mmlreference
pipenv run python /emwiki/emwiki/manage.py build_search_data
pipenv run python /emwiki/emwiki/manage.py load_articles
pipenv run python /emwiki/emwiki/manage.py load_symbols
