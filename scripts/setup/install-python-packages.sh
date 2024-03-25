#!/bin/bash

# Move to Working Directory
cd "$(dirname "$0")/../../mizcore"
touch "mizcore.cpython-39-x86_64-linux-gnu.so"
touch "py_miz_controller.cpython-39-x86_64-linux-gnu.so"

cd "build"
mkdir "lib.linux-x86_64-cpython-39"
cd "lib.linux-x86_64-cpython-39"
# touch "mizcore.cpython-39-x86_64-linux-gnu.so"

cd ../../
cat build/lib.linux-x86_64-3.9/py_miz_controller.cpython-39-x86_64-linux-gnu.so > py_miz_controller.cpython-39-x86_64-linux-gnu.so

cd "$(dirname "$0")/../../.."

# Main
pipenv sync --dev
