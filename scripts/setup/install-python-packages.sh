#!/bin/bash

# Move to Working Directory
cd "$(dirname "$0")/../../mizcore"

mkdir "build/lib.linux-x86_64-cpython-39"
touch "build/lib.linux-x86_64-cpython-39/mizcore.cpython-39-x86_64-linux-gnu.so"
cp "build/lib.linux-x86_64-3.9/py_miz_controller.cpython-39-x86_64-linux-gnu.so" "py_miz_controller.cpython-39-x86_64-linux-gnu.so"
cp "build/lib.linux-x86_64-cpython-39/py_miz_controller.cpython-39-x86_64-linux-gnu.so" "py_miz_controller.cpython-39-x86_64-linux-gnu.so"

cd "$(dirname "$0")/../../.."

# Main
pipenv sync --dev
