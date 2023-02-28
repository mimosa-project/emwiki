#!/bin/bash

# Move to Working Directory
cd "$(dirname "$0")/../.."

# Main
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get install -y cmake libpq-dev libssl-dev libffi-dev libfl-dev pbzip2 graphviz build-essential flex bison
sudo curl -sL https://deb.nodesource.com/setup_16.x | sudo bash -
python -m pip install --upgrade pip
sudo pip install pipenv --upgrade
sudo apt-get install -y nodejs
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
