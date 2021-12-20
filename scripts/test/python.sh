#!/bin/bash

# Move to Working Directory
cd "$(dirname "$0")/../../emwiki"

# Main
pipenv run coverage run
