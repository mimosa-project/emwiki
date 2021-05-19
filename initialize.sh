#!/bin/sh
# sh initialize.sh

MIZFILE_DIR="emwiki/mizarfiles"
MIZAR_VERSION="5.57.1355"

if [ -e .env ]; then
    . .devcontainer/.env
    echo 'Loaded environment from .env'
else :
fi


read_and_check() {
    while :
    do
        read str
        if [ $str = 'y' -o $str = 'n' ]; then
            break
        fi
        echo 'Please enter "y" or "n"'
    done
}


## ask about mizar files
remove_mizarfiles='n'
echo "Do you want to download all mizarfiles?(y/n)"
read_and_check
initialize_for_mizarfiles=$(echo $str)
if [ $initialize_for_mizarfiles = 'y' ]; then
    
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
else
    echo "If you want to keep mizarfiles, type y.\nIf you want to delete all mizarfiles, type n.(y/n)"
    read_and_check
    if [ $str = 'n' ]; then
        echo "removing all mizarfiles"
        rm -rf ${MIZFILE_DIR}/abstr
        rm -rf ${MIZFILE_DIR}/vct
        rm -rf emwiki/templates/article/fmbibs
        rm -rf ${MIZFILE_DIR}/htmlized_mml
        exit 0
    fi
fi
            
## ask about emparser
echo "Do you want to clone emparser?(y/n)"
read_and_check
initialize_for_emparser=$(echo $str)

## ask about emwiki-contents
echo "Do you want to clone emwiki-contents?(y/n)"
read_and_check
initialize_for_emwiki_contents=$(echo $str)

## ask about pipfile.lock
echo "Do you want to sync with Pipfile.lock?(y/n)"
read_and_check
initialize_for_pipfile_lock=$(echo $str)

## ask about migrate
echo "Do you want to migrate?(y/n)"
read_and_check
migrate_for_emwiki=$(echo $str)

## ask about emwiki files
echo "Do you want to generate emwiki files?(y/n)"
read_and_check
initialize_for_emwiki_files=$(echo $str)

# execution

## download mizar files
if [ $initialize_for_mizarfiles = 'y' ]; then
    ### abstr, vct, fmbibs
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

    ### htmlized mml
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
fi

## git clone emparser
if [ $initialize_for_emparser = 'y' ]; then
    git clone --recursive https://github.com/mimosa-project/emparser.git ./emparser
fi

## git clone emwiki-contents
if [ $initialize_for_emwiki_contents = 'y' ]; then
    git clone -b ${COMMENT_COMMIT_BRANCH} ${COMMENT_REPOSITORY_URL} ${MIZFILE_DIR}/emwiki-contents
fi

## pipenv sync
if [ $initialize_for_pipfile_lock = 'y' ]; then
    pipenv sync
fi

## migrate for emwiki
if [ $migrate_for_emwiki = 'y' ]; then
    pipenv run python ./emwiki/manage.py createcachetable
    pipenv run python ./emwiki/manage.py migrate
fi

## generate files for emwiki
if [ $initialize_for_emwiki_files = 'y' ]; then
    pipenv run python ./emwiki/manage.py build_htmlizedmml
    pipenv run python ./emwiki/manage.py build_mmlreference
    pipenv run python ./emwiki/manage.py build_search_data
    pipenv run python ./emwiki/manage.py load_articles
    pipenv run python ./emwiki/manage.py load_symbols
fi