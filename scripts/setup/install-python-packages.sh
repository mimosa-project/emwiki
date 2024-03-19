#!/bin/bash

# Move to Working Directory
cd "$(dirname "$0")/../../mizcore/build/lib.linux-x86_64-cpython-39"
echo dir: $(pwd)
touch mizcore.cpython-39-x86_64-linux-gnu.so

cd "$(dirname "$0")/../../../../.."
ls
echo dir: $(pwd)

# Main
pipenv sync --dev
