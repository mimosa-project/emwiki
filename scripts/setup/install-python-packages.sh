#!/bin/bash

# Move to Working Directory
cd "$(dirname "$0")/../../mizcore/build"
ls
# cd "$(dirname "$0")/../../mizcore/build/lib.linux-x86_64-3.9"
mkdir -p "$(dirname "$0")/../../mizcore/build/lib.linux-x86_64-cpython-39"
ls
touch mizcore.cpython-39-x86_64-linux-gnu.so
# ls

cd "$(dirname "$0")/../.."

# Main
pipenv sync --dev
