#!/bin/sh

if [ $1 = "dev" -a -e .devcontainer/.env ]; then
    . .devcontainer/.env
    echo 'Loaded environment from .devcontainer/.env'
elif [ $1 = "prod" -a -e .prodcontainer/.env ]; then
    . .prodcontainer/.env
    echo 'Loaded environment from .prodcontainer/.env'
else
    echo 'NO .env or .devcontainer/.env Detected or Not specifyed "dev" or "prod"'
    exit
fi

if [ ! -d emwiki/mizarfiles/htmlized_mml ]; then
    mkdir -p htmlized_mml
    echo 'Downloading new HTMLized_MML'
    wget https://ftp.icm.edu.pl/packages/mizar/xmlmml/html_abstr.5.57.1355.tar.gz -O ./htmlized_mml/htmlized_mml.tar.gz
    echo 'Extracting new HTMLized_MML'
    tar -zxf ./htmlized_mml/htmlized_mml.tar.gz -C htmlized_mml
    echo 'Removing old HTMLized_MML'
    rm -r emwiki/mizarfiles/htmlized_mml
    echo 'Moving new HTMLized_MML'
    mv -i htmlized_mml/html emwiki/mizarfiles/htmlized_mml
    echo 'Remoing chaches'
    rm -r htmlized_mml
else
    echo 'HTMLized MML Directory already exists'
fi

if [ ! -d emwiki/mizarfiles/abstr ]; then
    mkdir temp
    echo 'Downloading new mizar-data'
    wget http://mizar.uwb.edu.pl/~softadm/current/mizar-8.1.09_5.57.1355-arm-linux.tar -O temp/mizar.tar
    echo 'Extracting abstrfiles for search_theorem'
    tar -xf temp/mizar.tar -C temp
    tar -zxf temp/mizshare.tar.gz -C temp
    echo 'Converting abstr files to utf-8'
    ulimit -n 2048
    nkf -w --overwrite temp/abstr/*.abs
    echo 'Removing old abstrfiles and data for search_theorem'
    rm -r emwiki/mizarfiles/abstr
    rm -r emwiki/mizarfiles/vct
    rm -r emwiki/search/data
    echo 'Moving abstrfiles for search_theorem'
    mkdir emwiki/mizarfiles/abstr
    mv temp/abstr/*.abs emwiki/mizarfiles/abstr
    mkdir emwiki/mizarfiles/vct
    mv temp/mml.vct emwiki/mizarfiles/vct
    mkdir emwiki/search/data
    echo 'Remoing chaches'
    rm -r temp
else
    echo 'data for search_theorem already exists'
fi

echo 'Cloning emwiki-contents'
git clone -b $COMMENT_COMMIT_BRANCH $COMMENT_REPOSITORY_URL emwiki/mizarfiles/emwiki-contents
