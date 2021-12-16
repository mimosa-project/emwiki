#!/bin/bash

# Move to Working Directory
cd "$(dirname "$0")/../.."

# Main
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get install -y cmake libpq-dev python3.7-dev libssl-dev libffi-dev pbzip2 graphviz python3-pip
sudo curl -sL https://deb.nodesource.com/setup_16.x | sudo bash -
sudo pip install pipenv --upgrade
sudo apt-get install -y nodejs
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
