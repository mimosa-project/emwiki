#!/bin/bash

# Move to Working Directory
cd "$(dirname "$0")/../../mizcore"

# Main
python setup.py build
ls