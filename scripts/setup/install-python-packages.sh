#!/bin/bash

# Move to Working Directory
cd "$(dirname "$0")/../../mizcore"
# touch "mizcore.cpython-39-x86_64-linux-gnu.so"
# touch "py_miz_controller.cpython-39-x86_64-linux-gnu.so"
ls -a
cd "lib.linux-x86_64-3.9"
echo "create lib.linux-x86_64-3.9"
ls -a
# echo "mizcore.cpython-39-x86_64-linux-gnu.so" > "mizcore.pth"


cd "build"
ls -a
mkdir "lib.linux-x86_64-cpython-39"

cd "lib.linux-x86_64-cpython-39"
# touch "mizcore.cpython-39-x86_64-linux-gnu.so"

cd "$(dirname "$0")/../../.."

# Main
pipenv sync --dev
