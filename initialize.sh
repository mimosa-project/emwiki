#!/bin/sh
# sh initialize.sh

MIZFILE_DIR="emwiki/mizarfiles"
MIZAR_VERSION="5.57.1355"

download_mizarfiles() {
    # check files exists 
    if [ -d $MIZFILE_DIR/abstr ]; then
        echo "abstr files already exists"
        exit 1
    elif [ -d $MIZFILE_DIR/vct ]; then
        echo "vct files already exists"
        exit 1
    elif [ -d emwiki/templates/article/fmbibs ]; then
        echo "fmbibs files already exists"
        exit 1
    elif [ -d $MIZFILE_DIR/htmlized_mml ]; then
        echo "htmlized_mml files already exists"
        exit 1
    fi
    # download
    ## abstr, vct, fmbibs
    echo "creating abstr, vct, fmbibs"
    echo "dowmloading abstr, vct, fmbibs"
    mkdir -p ./temp
    wget http://mizar.uwb.edu.pl/~softadm/current/mizar-8.1.09_${MIZAR_VERSION}-arm-linux.tar -O ./temp/mizar.tar
    echo "Extracting new abstr, vct, fmbibs"
    tar -xf ./temp/mizar.tar -C ./temp
    tar -zxf ./temp/mizshare.tar.gz -C ./temp
    tar -zxf ./temp/mizdoc.tar.gz -C ./temp
    unzip -q ./temp/fmbibs.zip -d ./temp/fmbibs
    echo "Converting abstr files to utf-8"
    ulimit -n 2048
    nkf -w --overwrite ./temp/abstr/*.abs
    echo "moving new abstr, vct, fmbibs"
    mkdir -p ${MIZFILE_DIR}/abstr
    mv ./temp/abstr/*.abs ${MIZFILE_DIR}/abstr
    mkdir ${MIZFILE_DIR}/vct
    mv ./temp/mml.vct ${MIZFILE_DIR}/vct/mml.vct
    mkdir -p emwiki/templates/article/fmbibs
    mv ./temp/fmbibs/*.bib emwiki/templates/article/fmbibs
    echo "Remoing chaches"
    rm -rf ./temp
    ## htmlized mml
    echo "creating htmlized_mml"
    mkdir -p ./temp
    wget https://ftp.icm.edu.pl/packages/mizar/xmlmml/html_abstr.${MIZAR_VERSION}.tar.gz -O ./temp/htmlized_mml.tar.gz
    echo "Extracting new HTMLized_MML"
    tar -zxf ./temp/htmlized_mml.tar.gz -C ./temp
    echo "moving new HTMLized_MML"
    mkdir ${MIZFILE_DIR}/htmlized_mml
    mv ./temp/html/* ${MIZFILE_DIR}/htmlized_mml
    echo "Remoing chaches"
    rm -rf ./temp
}

remove_allmizarfiles() {
    echo "removing all mizarfiles"
    rm -rf ${MIZFILE_DIR}/abstr
    rm -rf ${MIZFILE_DIR}/vct
    rm -rf emwiki/templates/article/fmbibs
    rm -rf ${MIZFILE_DIR}/htmlized_mml
}

# check the argument and Load environment variable
if [ $1 = "dev" -a -e ./.env ]; then
    . ./.env
    echo 'Loaded environment from .devcontainer/.env'
elif [ $1 = "prod" -a -e .prodcontainer/.env ]; then
# elif [ $1 = "prod" -a -e .prodcontainer/.env ]; then
    . .prodcontainer/.env
    echo 'Loaded environment from .prodcontainer/.env'
elif [ $1 = "rm" ]; then
    remove_allmizarfiles
    exit
else
    echo 'NO .env or .prodcontainer/.env Detected or Not specifyed "dev" or "prod"'
    exit
fi

# setup

download_mizarfiles

git clone --recursive https://github.com/mimosa-project/emparser.git ./emparser
git clone -b ${COMMENT_COMMIT_BRANCH} ${COMMENT_REPOSITORY_URL} ${MIZFILE_DIR}/emwiki-contents

## create a virtual environment
pipenv sync

## migrate for emwiki
pipenv run python ./emwiki/manage.py createcachetable
pipenv run python ./emwiki/manage.py migrate

## generate files for emwiki
pipenv run python ./emwiki/manage.py build_htmlizedmml
pipenv run python ./emwiki/manage.py build_mmlreference
pipenv run python ./emwiki/manage.py build_search_data
pipenv run python ./emwiki/manage.py load_articles
pipenv run python ./emwiki/manage.py load_symbols

## prod only
if [ $1 = "prod" ]; then
  pipenv run uwsgi --chdir=/workspace/emwiki/ --mount /emwiki=/workspace/emwiki/emwiki/wsgi.py --manage-script-name --env DJANGO_SETTINGS_MODULE=emwiki.settings --socket :8001
fi