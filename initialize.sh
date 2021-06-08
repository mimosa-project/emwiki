#!/bin/sh
# sh initialize.sh

# 注意点
# **MML, HTMLized MML のMMLバージョンは必ず統一すること．**
# **MML(.miz, .abs)をHP等からDownloadする際にはutf-8に変換を行うこと**

# initialize.shについて

## initialize.sh {引数}を実行すると初期設定が行われます. 設定を変更したい場合はinitialize.shを書き換えてください
## initialize.shを実行したときに、Mizarファイルが既に存在する場合はエラーが出力され、Mizarファイルがダウンロードされません. 
## この場合は一度"rm"オプションをつけて実行し, 再度実行してください.

### 引数"dev"は開発環境構築用の処理が行われます
### 引数"prod1"は本番環境構築用の処理(RUN命令で呼び出される)が行われます
### 引数"prod2"は本番環境構築用の処理(ENTRYPOINT命令で呼び出される)が行われます
### 引数"rm"では既に存在するMizarファイルを削除する処理が行われます.


MIZFILE_DIR="emwiki/mizarfiles"

# emwikiで使用するMizarファイル等を自動でダウンロードし, 解凍, 文字コードの変換, 敵切な場所への配置を行う
download_mizarfiles() {
    # check files exists 
    if [ -d $MIZFILE_DIR/abstr ]; then
        echo "abstr files already exists"
        exit 1
    elif [ -d $MIZFILE_DIR/vct ]; then
        echo "vct files already exists"
        exit 1
    elif [ -d emwiki/article/templates/article/fmbibs/ ]; then
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
    mkdir -p emwiki/article/templates/article/fmbibs/
    mv ./temp/fmbibs/*.bib emwiki/article/templates/article/fmbibs/
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

remove_all_mizarfiles() {
    echo "removing all mizarfiles"
    rm -rf ${MIZFILE_DIR}/abstr
    rm -rf ${MIZFILE_DIR}/vct
    rm -rf emwiki/article/templates/article/fmbibs/
    rm -rf ${MIZFILE_DIR}/htmlized_mml
}


if [ $1 = "dev" -o $1 = "prod1" -o $1 = "prod2" ]; then
    # 環境変数の読み込み
    . ./.env
    echo 'Loaded environment from .env'
fi

if [ $1 = "dev" -o $1 = "prod1" ]; then
    # setup
    apt-get -y update
    apt-get -y upgrade
    apt-get -y install cmake libpq-dev nkf unzip 
    pip -q install pipenv
    download_mizarfiles
    git clone --recursive https://github.com/mimosa-project/emparser.git ./emparser
    git clone -b ${COMMENT_COMMIT_BRANCH} ${COMMENT_REPOSITORY_URL} ${MIZFILE_DIR}/emwiki-contents
    pipenv sync
    pipenv run python ./emwiki/manage.py build_htmlizedmml
    pipenv run python ./emwiki/manage.py build_mmlreference
    pipenv run python ./emwiki/manage.py build_search_data

fi

if [ $1 = "dev" -o $1 = "prod2" ]; then
    # データベースが立った後の処理
    pipenv run python ./emwiki/manage.py migrate
    pipenv run python ./emwiki/manage.py load_articles
    pipenv run python ./emwiki/manage.py load_symbols
fi

if [ $1 = "prod2" ]; then
    pipenv run uwsgi --chdir=/workspace/emwiki/ --mount /emwiki=/workspace/emwiki/emwiki/wsgi.py --manage-script-name --env DJANGO_SETTINGS_MODULE=emwiki.settings --socket :8001
fi

if [ $1 = "rm" ]; then
    remove_all_mizarfiles
    exit
fi
