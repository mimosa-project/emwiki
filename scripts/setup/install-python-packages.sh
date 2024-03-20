#!/bin/bash

# Move to Working Directory
cd "$(dirname "$0")/../../mizcore"
touch mizcore.cpython-39-x86_64-linux-gnu.so
ls

echo "Change directory to build"
cd "build"
ls

mkdir "lib.linux-x86_64-cpython-39"
echo "Created lib.linux-x86_64-cpython-39"
ls
cd "lib.linux-x86_64-cpython-39"
touch mizcore.cpython-39-x86_64-linux-gnu.so
echo "Created mizcore.cpython-39-x86_64-linux-gnu.so"
ls

cd "$(dirname "$0")/../../.."

# Main
pipenv sync --dev
