#!/bin/sh

if [ -e .env ]; then
    . .env
    echo 'Loaded environment from .env'
elif [ -e .devcontainer/.env ]; then
    . .devcontainer/.env
    echo 'Loaded environment from .devcontainer.env'
else
    echo 'NO .env or .devcontainer/.env Detected'
    exit
fi

if [ ! -d emwiki/contents/mizarfiles/htmlized_mml ]; then
    mkdir -p htmlized_mml
    echo 'Downloading new HTMLized_MML'
    wget https://ftp.icm.edu.pl/packages/mizar/xmlmml/html_abstr.5.57.1355.tar.gz -O ./htmlized_mml/htmlized_mml.tar.gz
    echo 'Extracting new HTMLized_MML'
    tar -zxf ./htmlized_mml/htmlized_mml.tar.gz -C htmlized_mml
    echo 'Removing old HTMLized_MML'
    rm -r emwiki/contents/mizarfiles/htmlized_mml
    echo 'Moving new HTMLized_MML'
    mv -i htmlized_mml/html emwiki/contents/mizarfiles/htmlized_mml
    echo 'Remoing chaches'
    rm -r htmlized_mml
else
    echo 'HTMLized MML Directory already exists'
fi

echo 'Cloning emwiki-contents'
git clone -b $COMMENT_PUSH_BRANCH $COMMENT_REPOSITORY_URL emwiki/contents/mizarfiles/emwiki-contents
