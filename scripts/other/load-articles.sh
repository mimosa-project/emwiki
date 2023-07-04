#!/bin/bash

# Move to Working Directory
cd "$(dirname "$0")/../.."

# Main
pipenv run python emwiki/manage.py load_articles
