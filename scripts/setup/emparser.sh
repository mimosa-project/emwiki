#!/bin/bash

# Move to Working Directory
cd "$(dirname "$0")/../../emparser"

# Main
pipenv install --python 3.7
pipenv run python setup.py build
