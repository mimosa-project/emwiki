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
written on [pipfile](https://github.com/mimosa-project/emwiki/blob/master/Pipfile)

### emparser
emparserのインストールが必要です.
#### Git clone
```
git clone --recursive https://github.com/mimosa-project/emparser.git
```
#### Setup development environment
```
resolve importlib- conflict
pipenv install
```
#### Install
```
install cmake
python setup.py install
```
## 4 Install
### 4.1 ホストの準備
docker, docker-composeをインストール
+ [Get Docker](https://docs.docker.com/get-docker/)
+ WSL2を用いる場合はDocker Desktop for Windowsをインストール

GitHubで、[mimosa-project/emwiki](https://github.com/mimosa-project/emwiki)をForkする

git clone
```
git clone {your forked origin repository}
```

### 4.2 .envファイルを更新
#### 開発環境
+ `.devcontainer/.env`を、`.devcontainer/.env-sample`を元に新たに作成する
  + **(must)**`COMMENT_REPOSITORY_URL`を再設定する
    + [mimosa-project/emwiki-contents](https://github.com/mimosa-project/emwiki-contents)をForkして、ForkしたレポジトリのURLに書き換える
  + その他の変更は、原則必要なし
+ `.devcontainer/.env.db`を、`.devcontainer/.env.db-sample`を元に新たに作成する
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
  + その他の設定を適宜再設定
+ `.env.db`を、`.env.db-sample`を元に新たに作成
  + **(must)**`.env`に設定した`SQL_USER`の値を`POSTGRES_USER`に設定
  + **(must)**`.env`に設定した`SQL_PASSWORD`の値を`POSTGRES_PASSWORD`に設定
+ `docker-compose.yml`内のhttps-portalを変更
  + **(must)**`DOMAINS: 'localhost->http://nginx:8000'`の`localhost`を、デプロイするドメインに変更
  + **(must)**`STAGE: 'production'`をコメントから外す


### 4.3 必要ファイルの追加
+ 開発環境、本番環境の、いずれかの方法でファイルを追加する
+ 最後に確認事項を読み、ファイルの存在を確認する
  + なければを手動で追加する際の注意点を参考に、手動でファイルを追加する
#### 開発環境
+ .devcontainer/.envを使用する
  + 必ず先に`.devcontainer/.env`を作成する
  ```
  sh initialize.sh dev
  ```
#### 本番環境
+ .prodcontainer/.envを使用する
  + 必ず先に`.prodcontainer/.env`を作成する
  ```
  sh initialize.sh prod
  ```
#### 手動で追加する際の注意点
+ **MML, HTMLized MML のMMLバージョンは必ず統一すること．**
+ **MML(.miz, .abs)をHP等からDownloadする際にはutf-8に変換を行うこと**
+ `initialize.sh <env file>`を実行する事で、必要ファイルのDLが完了する

#### 確認事項
+ 以下のディレクトリにMMLファイル、HTMLized MMLファイル、absrtファイル、vctファイルがあることを確認する
  + `project_dir/emwiki/contents/mizarfiles/emwiki-contents/mml/{*.miz}`
  + `project_dir/emwiki/contents/mizarfiles/htmlized_mml/{*.html}`
  + `project_dir/emwiki/contents/mizarfiles/abstr/{*.abs}`
  + `project_dir/emwiki/contents/mizarfiles/vct/mml.vct`
+ 以下のディレクトリを作成する
  + `emwiki/search/data`

### 4.4コンテナの作成
#### 開発環境
+ 必要ファイルは`.devcontainer`の中にある
+ VSCodeの拡張機能`ms-vscode-remote.remote-containers`を用いることで簡単に行うことができる
+ 時間がかかる点に注意．
```
cd .devcontainer
docker-compose up -d --build
```
+ 以下をコンテナ内で実行
  + superuserの作成
    ```
    python manage.py createsuperuser
    ```
  + エラーが出る場合、以下のインタプリタが設定されているか確認する
    ```
    /usr/local/bin/python
    ```
+ 独自コマンド(実行する必要なし)
  + MML, HTMLizedMMLファイルの加工
  ```
  python manage.py generate_files all
  ```
  + Article, Comment, Symbolの登録
  ```
  python manage.py register_db all
  ```

+ コンテナ作成・起動後、実行方法は通常通り(コンテナ内で実行)
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
### 4.5 終了
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
+ `/emwiki/contents/mizarfiles/emwiki-contents/mml`を新しいMMLと交換する
+ add, commit(commitメッセージにバージョン情報をつける)
+ `mml_commented`ブランチにcheckoutする
+ 新たな`mml`ブランチの変更を`mml_commented`ブランチにマージする
### 5.2 HTMLized MML
+ [ここ](https://ftp.icm.edu.pl/packages/mizar/xmlmml/)からDL可能
+ emwiki-contentsのバージョンと統一させる
+ `project_dir/emwiki/contents/mizarfiles/htmlized_mml/{*.html}`に配置する
+ `initialize.sh`を書き換える
### 5.3 data for search theorem
+ 定理検索を使用するには`project_dir/emwiki/search/data/`内にabsファイルとvctファイルから生成されるデータが必要
+ absファイルとvctファイルはMizarをダウンロードすることで入手可能
+ データを生成するにはabsファイルとvctファイルをそれぞれ`project_dir/emwiki/contents/mizarfiles/abstr/{*.abs}`, `project_dir/emwiki/contents/mizarfiles/vct/mml.vct`に配置し, 以下のコマンドを実行(実行に時間がかかります)
  ```
  python manage.py generate_files search
  ```
+ absファイルとvctファイルのダウンロード等は, `initialize.sh`を書き換えることで行う
## 6 Buckup
### 6.1 emwiki-contents
+ pythonコンテナに入る
  + `docker exec <container name> bash`
+ emwiki-contentsのレポジトリに移動
  + `cd /workspace/emwiki/contents/mizarfiles/emwiki-contents`
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

