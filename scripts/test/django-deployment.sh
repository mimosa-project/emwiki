#!/bin/bash

# Move to Working Directory
cd "$(dirname "$0")/../../emwiki"

# Main
pipenv run python ./emwiki/manage.py check --deploy
