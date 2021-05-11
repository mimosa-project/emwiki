#!/bin/sh
# sh initialize.sh

# MIZAR_VERSION="5.57.1355"
MIZFILE_DIR="emwiki/mizarfiles"

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
    elif [ -d $MIZFILE_DIR/fmbibs ]; then
        echo "fmbibs files already exists"
        exit 1
    elif [ -d $MIZFILE_DIR/htmlized_mml ]; then
        echo "htmlized_mml files already exists"
        exit 1
    fi
else
    echo "Do you want to keep all mizarfiles?(y/n)"
    read_and_check
    if [ $str = 'n' ]; then
        echo "Do you want to remove all mizarfiles?(y/n)"
        read_and_check
        remove_mizarfiles=$(echo $str)
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
if [ $initialize_for_emwiki_contents = 'y' ]; then
    echo "Enter the url of the emwiki-contents repository"
    read COMMENT_REPOSITORY_URL
fi

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
    mkdir -p /temp
    wget http://mizar.uwb.edu.pl/~softadm/current/mizar-8.1.09_${MIZAR_VERSION}-arm-linux.tar -O /temp/mizar.tar
    echo "Extracting new abstr, vct, fmbibs"
    tar -xf /temp/mizar.tar -C /temp
    tar -zxf /temp/mizshare.tar.gz -C /temp
    tar -zxf /temp/mizdoc.tar.gz -C /temp
    unzip -q /temp/fmbibs.zip -d /temp/fmbibs
    echo "Converting abstr files to utf-8"
    ulimit -n 2048
    nkf -w --overwrite /temp/abstr/*.abs
    echo "moving new abstr, vct, fmbibs"
    mkdir -p ${MIZFILE_DIR}/abstr
    mv /temp/abstr/*.abs ${MIZFILE_DIR}/abstr
    mkdir ${MIZFILE_DIR}/vct
    mv /temp/mml.vct ${MIZFILE_DIR}/vct/mml.vct
    mkdir -p emwiki/templates/article/fmbibs
    mv /temp/fmbibs/*.bib emwiki/templates/article/fmbibs
    echo "Remoing chaches"
    rm -rf /temp

    ### htmlized mml
    echo "creating htmlized_mml"
    mkdir -p /temp
    wget https://ftp.icm.edu.pl/packages/mizar/xmlmml/html_abstr.${MIZAR_VERSION}.tar.gz -O /temp/htmlized_mml.tar.gz
    echo "Extracting new HTMLized_MML"
    tar -zxf /temp/htmlized_mml.tar.gz -C /temp
    echo "moving new HTMLized_MML"
    mkdir ${MIZFILE_DIR}/htmlized_mml
    mv /temp/html/* ${MIZFILE_DIR}/htmlized_mml
    echo "Remoing chaches"
    rm -rf /temp
fi

## remove mizar files
if [ $remove_mizarfiles = 'y' ]; then
    echo "removing all mizarfiles"
    rm -rf ${MIZFILE_DIR}/abstr
    rm -rf ${MIZFILE_DIR}/vct
    rm -rf emwiki/templates/article/fmbibs
    rm -rf ${MIZFILE_DIR}/htmlized_mml
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
    pipenv run python ./emwiki/manage.py makemigrations accounts
    pipenv run python ./emwiki/manage.py makemigrations article
    pipenv run python ./emwiki/manage.py makemigrations graph
    pipenv run python ./emwiki/manage.py makemigrations search
    pipenv run python ./emwiki/manage.py makemigrations symbol
    pipenv run python ./emwiki/manage.py migrate
    pipenv run python ./emwiki/manage.py createcachetable
fi

## generate files for emwiki
if [ $initialize_for_emwiki_files = 'y' ]; then
    pipenv run python ./emwiki/manage.py build_htmlizedmml article
    pipenv run python ./emwiki/manage.py build_mmlreference symbol
    pipenv run python ./emwiki/manage.py build_search_data search
    pipenv run python ./emwiki/manage.py load_articles
    pipenv run python ./emwiki/manage.py load_symbols
fi
