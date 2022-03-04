#!/bin/bash

# Move to Working Directory
cd "$(dirname "$0")/../.."

# Main
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get install -y cmake libpq-dev libssl-dev libffi-dev pbzip2 graphviz
sudo curl -sL https://deb.nodesource.com/setup_16.x | sudo bash -
python3.7 -m pip install --upgrade pip
sudo python3.7 -m pip install pipenv --upgrade
sudo apt-get install -y nodejs
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
