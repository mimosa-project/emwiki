#!/bin/bash

# Move to Working Directory
cd "$(dirname "$0")/../.."

# Main
sudo apt install build-essential  -y
sudo apt install libssl-dev zlib1g-dev libncurses5-dev libncursesw5-dev libreadline-dev libsqlite3-dev -y
sudo apt install libgdbm-dev libdb5.3-dev libbz2-dev libexpat1-dev liblzma-dev libffi-dev uuid-dev -y
wget https://www.python.org/ftp/python/3.7.10/Python-3.7.10.tgz
tar zxvf Python-3.7.10.tgz
cd Python-3.7.10/
./configure --enable-optimizations
make -j4
sudo make altinstall
cd ..
rm -rf Python-3.7.10
sudo apt install python3-pip
