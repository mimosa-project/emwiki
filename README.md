emwiki
====

Wiki for eco-Mizar

## 1 Description
This Web application can write a TeX-format description in the Mizar Mathmatical Library (MML), and make the description follow the MML update. This Web application provides users with the function of adding, editing, and browsing description of MML on a Wiki format Web platform. If there is an update to the MML, link the description to the new MML by running the program on the server.

## 2 Demo
+ Use HTMLized MML
  + Hyper Link
  + Hover tooltips
  + folding proof, etc.
+ Browsing, adding, editing comment of MML
+ Easy search
+ Version following
+ Many additional features are planned
  + Advanced search function
  + Dependency graph
  
  
![emwiki](https://user-images.githubusercontent.com/49423101/98566104-b8556900-22f1-11eb-89fb-662a353d0dcb.png)

## 3 Requirement
+ docker, docker-composeが必要です.
+ wslを用いて開発を行う場合は, pythonのバージョン3.7が必要です. 以下参考(https://hibiki-press.tech/python/install-from-source/5046)
+ wslを用いて開発を行う場合は, cmake, libpq-dev, nkf, unzip, pipenvが必要です.(Dockerのみで開発を行う場合には不要)

## 4 Install
### 4.1 ホストの準備
+ docker, docker-composeをインストール
  + [Get Docker](https://docs.docker.com/get-docker/)

+ GitHubで、[mimosa-project/emwiki](https://github.com/mimosa-project/emwiki)と[mimosa-project/emwiki-contents](https://github.com/mimosa-project/emwiki-contents)をForkする<br>
+ emwikiをgit cloneする<br>

```
git clone {your forked origin repository}
```
+ wslを用いて開発を行う場合は, cmake, libpq-dev, nkf, unzip, pipenvをインストール
```
apt-get -y update
apt-get -y upgrade
apt-get -y install cmake nkf unzip libpq-dev
pip -q install pipenv
```
### 4.2 .envファイルを更新
#### 開発環境
+ `.env`を,`.env-sample`を元に新たに作成
  + **(must)**`SECRET_KEY`をランダムな値に設定(50文字以上)
  + **(must)**`COMMENT_REPOSITORY_URL`を再設定する
    + [mimosa-project/emwiki-contents](https://github.com/mimosa-project/emwiki-contents)をForkしたレポジトリのURLに書き換える
  + wslを使った開発環境では`SQL_HOST`の値を`localhost`に設定(Dockerのみで開発を行う場合には原則変更不要)
  + その他の変更は、原則必要なし
+ データベースの設定ファイルを変更する場合は, docker-compose.ymlのdb部分のenvironment部を書き換える
  + 変更は、原則必要なし
#### 本番環境
+ `.env`を、`.env-sample`を元に新たに作成
  + **(must)**`DEBUG=False`に設定
  + **(must)**`SECRET_KEY`をランダムな値に設定(50文字以上)
  + **(must)**`DJANGO_ALLOWED_HOSTS`を、デプロイするホストに設定
  + **(must)**`COMMENT_REPOSITORY_URL`を再設定
  + **(must)**`COMMENT_COMMIT_BRANCH`を`mml_commented`に設定
  + **(must)**`SQL_USER`を再設定
  + **(must)**`SQL_PASSWORD`を再設定
  + **(must)**`MIZAR_VERSION`を再設定
  + その他の設定を適宜再設定
+ `.env.db`を、`.env.db-sample`を元に新たに作成
  + **(must)**`.env`に設定した`SQL_USER`の値を`POSTGRES_USER`に設定
  + **(must)**`.env`に設定した`SQL_PASSWORD`の値を`POSTGRES_PASSWORD`に設定
+ `docker-compose.yml`内のhttps-portalを変更
  + **(must)**`DOMAINS: 'localhost->http://nginx:8000'`の`localhost`を、デプロイするドメインに変更
  + **(must)**`STAGE: 'production'`をコメントから外す

### 4.3コンテナの作成
#### 開発環境
+ 必要ファイルは`.devcontainer`の中にある
+ VSCodeの拡張機能`ms-vscode-remote.remote-containers`を用いることで簡単に行うことができる
+ 時間がかかる点に注意．
```
cd .devcontainer
docker-compose up -d --build
```
+ 以下をコンテナ内で実行
  + 初期設定(初回のみの実行で良い)
  ```
  sh initialize.sh
  ```
    初回はすべてyを入力.<br>
    実行例
    ```
    root ➜ /workspace (Master ✗) $ sh initialize.sh
    Do you want to download all mizarfiles?(y/n)
    y
    Do you want to clone emparser?(y/n)
    y
    Do you want to clone emwiki-contents?(y/n)
    y
    Do you want to sync with Pipfile.lock?(y/n)
    y
    Do you want to migrate?(y/n)
    y
    Do you want to generate emwiki files?(y/n)
    y
    ```
  + pipenvの仮想環境に入る
  ```
  pipenv shell
  ```
  + superuserの作成
  ```
  python manage.py createsuperuser
  ```
+ 独自コマンド(実行する必要なし)
  + MML, HTMLizedMMLファイルの加工
  ```
  python manage.py build_htmlizedmml
  python manage.py build_mmlreference
  python manage.py build_search_data
  ```
  + Article, Comment, Symbolの登録
  ```
  python manage.py load_articles
  python manage.py load_symbols
  ```

+ コンテナ作成・起動後、実行方法は通常通り(コンテナ内で実行)
  ```
  python manage.py runserver
  ```

#### wslを使った開発環境
+ pythonコンテナを使わず, wslを使用する場合は, `.devcontainer/docker-compose.yml`ファイルのpython部分を削除する.
```
version: '3'

services:
  db:
    image: postgres:latest
    restart: unless-stopped
    volumes:
      - ./postgres-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=postgres

  # Add "forwardPorts": ["5432"] to **devcontainer.json** to forward PostgreSQL locally.
  # (Adding the "ports" property to this file will not forward from a Codespace.)


  adminer:
    image: adminer:latest
    restart: unless-stopped
    ports: 
      - 8080:8080
    depends_on: 
      - db
```
+ `.env`ファイルをpipfileと同じディレクトリに移動する(プロジェクトディレクトリの下).
```
project_dir/.env
```
+ `.devcontainer`に移動し, dbコンテナとadmirコンテナを立ち上げる
```
cd .devcontainer
docker-compose up -d --build
```
+ コンテナを立ち上げ, プロジェクトのルートディレクトリに戻り`initialize.sh`を実行(初回のみ)
+ `initialize.sh`を実行する前に, 以下のことを確認する.
  + 自分の環境に, cmake, libpq-dev, nkf, unzip, pipenvがインストールされていること
  + 同じ階層に`.env`ファイルが存在すること
  + `.env`ファイルの`SQL_HOST`の値が`localhost`に設定されていること
  + sudoで実行すること
  ```
  cd ..
  sudo sh initialize.sh
  ```
初回はすべてyを入力.<br>
  実行例

    ```
    (emwiki) g063ff@DESKTOP-2RPAO3O:~/emwiki$ sudo sh initialize.sh
    [sudo] password for g063ff: 
    Loaded environment from .env
    Do you want to download all mizarfiles?(y/n)
    y
    Do you want to clone emparser?(y/n)
    y
    Do you want to clone emwiki-contents?(y/n)
    y
    Do you want to sync with Pipfile.lock?(y/n)
    y
    Do you want to migrate?(y/n)
    y
    Do you want to generate emwiki files?(y/n)
    y
    ```
+ pipenvの仮想環境に入る
```
pipenv shell
```
+ superuserの作成
```
python manage.py createsuperuser
```
+ 実行
```
python manage.py runserver
```

#### 本番環境
+ 時間がかかる点に注意．
+ 実行後、5分程度待つ(uwsgiの起動を待つため)
```
docker-compose up -d --build
```
+ superuserの作成
```
docker-compose exec python python /workspace/emwiki/manage.py createsuperuser
```

### 4.4 必要ファイルの追加
+ 前の項目で`sh initialize.sh`を実行していれば, 特に操作は必要なし
+ 開発環境、本番環境の、いずれかの方法でファイルを追加する
+ 最後に確認事項を読み、ファイルの存在を確認する
  + なければ手動で追加する際の注意点を参考に、手動でファイルを追加する
#### 手動で追加する際の注意点
+ **MML, HTMLized MML のMMLバージョンは必ず統一すること．**
+ **MML(.miz, .abs)をHP等からDownloadする際にはutf-8に変換を行うこと**

#### 確認事項
+ 以下のディレクトリにMMLファイル、HTMLized MMLファイル、absrtファイル、vctファイルがあることを確認する
  + `project_dir/emwiki/mizarfiles/emwiki-contents/mml/{*.miz}`
  + `project_dir/emwiki/mizarfiles/htmlized_mml/{*.html}`
  + `project_dir/emwiki/mizarfiles/abstr/{*.abs}`
  + `project_dir/emwiki/mizarfiles/vct/mml.vct`
  + `project_dir/emwiki/templates/article/fmbibs/{*.bib}`
+ 以下のディレクトリにabs_dictionary.txt等のファイルが11件あることを確認する
  + `emwiki/search/data`

#### initialize.shについて
+ initialize.shを実行すると初期設定が行われます. 初回実行時はすべてyを入力してください. 
  + Do you want to download all mizarfiles?(y/n)<br>
   yを入力するとemwikiで使用するMizarファイル等を自動でダウンロードし, 解凍, 文字コードの変換, 敵切な場所への配置を行います.<br>
   すでにMizarファイルが存在する場合は終了します.<br>
   nを入力すると, 現在存在するMizarファイルを残しておくか, 削除するか質問されます. 残す場合はy, 削除する場合はnを入力してください.

  + Do you want to clone emparser?(y/n)<br>
   yを入力するとemparserがcloneされます.

  + Do you want to clone emwiki-contents?(y/n)<br>
   yを入力すると.envファイルに記述した`COMMENT_REPOSITORY_URL`の`COMMENT_COMMIT_BRANCH`のブランチからemwiki-contentsがcloneされます.

  + Do you want to migrate?(y/n)<br>
   yを入力すると, キャッシュテーブルの作成と, マイグレーションが行われます.

  + Do you want to generate emwiki files?(y/n)<br>
   yを入力すると, ダウンロードしたMizarファイル等からemwikiの実行に必要なファイルが生成されます.

### 4.6 終了
```
docker-compose down
```
### 4.6 永続化データ
#### 開発環境
+ コード全体: ./
+ Postgres Data: postgres-data
+ emwiki-contentsは、.devcontainer/.envに指定したレポジトリに自動的にPushされる
#### 本番環境
+ コード全体: ./
+ Postgres Data: postgres-data
+ static Data: static-volume
+ media Data: media-volume
+ emwiki-contents: emwiki-contents-volume
+ nginx設定ファイル: nginx/nginx.conf
+ uwsgi params: nginx/uwsgi_params
+ emwiki-contentsは、.envに指定したレポジトリに自動的にPushされる

## 5 Update MML version
+ emwiki内のコンテンツは，MMLとHTMLizedMMLを用いて作成されています．
+ MMLとHTMLizedMMLのバージョンは，**必ず一致させてください．**
### 5.1 emwiki-contents
+ `mml`ブランチにcheckoutする
+ `/emwiki/mizarfiles/emwiki-contents/mml`を新しいMMLと交換する
+ add, commit(commitメッセージにバージョン情報をつける)
+ `mml_commented`ブランチにcheckoutする
+ 新たな`mml`ブランチの変更を`mml_commented`ブランチにマージする
### 5.2 HTMLized MML
+ [ここ](https://ftp.icm.edu.pl/packages/mizar/xmlmml/)からDL可能
+ emwiki-contentsのバージョンと統一させる
+ `project_dir/emwiki/mizarfiles/htmlized_mml/{*.html}`に配置する
+ `initialize.sh`を書き換える
### 5.3 data for search theorem
+ 定理検索を使用するには`project_dir/emwiki/search/data/`内にabsファイルとvctファイルから生成されるデータが必要
+ absファイルとvctファイルはMizarをダウンロードすることで入手可能
+ データを生成するにはabsファイルとvctファイルをそれぞれ`project_dir/emwiki/mizarfiles/abstr/{*.abs}`, `project_dir/emwiki/mizarfiles/vct/mml.vct`に配置し, 以下のコマンドを実行(実行に時間がかかります)
  ```
  python manage.py generate_files search
  ```
+ absファイルとvctファイルのダウンロード等は, `initialize.sh`を書き換えることで行う
## 6 Buckup
### 6.1 emwiki-contents
+ pythonコンテナに入る
  + `docker exec <container name> bash`
+ emwiki-contentsのレポジトリに移動
  + `cd /workspace/emwiki/mizarfiles/emwiki-contents`
+ 上のリポジトリに移動してGitのPushを実行
  + `git push origin mml_commented`

### 6.2 PostgreSQL data
+ 以下のファイルをコピーしておく
  + 復元時には以下のディレクトリにバックアップしたデータを置きコンテナを立ち上げる
+ 開発環境
  + `.devcontainer/postgres-data`
+ 本番環境
  + `.prodcontainer/postgres-data`


## 7 Licence

![MIT License](https://github.com/mimosa-project/emwiki/blob/master/LICENSE)

