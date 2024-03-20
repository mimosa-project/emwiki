#!/bin/bash

# Move to Working Directory
cd "$(dirname "$0")/../../mizcore"
touch "mizcore.cpython-39-x86_64-linux-gnu.so"
# touch "py_miz_controller.cpython-39-x86_64-linux-gnu.so"
ls


cd "build"
mkdir "lib.linux-x86_64-cpython-39"

cd "lib.linux-x86_64-cpython-39"
echo "Creating MizCore Shared Object"
touch "mizcore.cpython-39-x86_64-linux-gnu.so"
touch "py_miz_controller.cpython-39-x86_64-linux-gnu.so"
ls

cd "$(dirname "$0")/../../.."

# Main
pipenv sync --dev
