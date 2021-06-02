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
### 動作環境
+ WSL(Ubuntu20.04) + Docker(PostgreSQL) (開発用)
+ Docker only (本番用)

## 4 Install
### 4.1 ホストの準備
+ docker, docker-composeをインストール
  + [Get Docker](https://docs.docker.com/get-docker/)

+ GitHubで、[mimosa-project/emwiki](https://github.com/mimosa-project/emwiki)と[mimosa-project/emwiki-contents](https://github.com/mimosa-project/emwiki-contents)をForkする<br>
+ emwikiをgit cloneする<br>
```
git clone {your forked origin repository}
```
+ cmake, libpq-dev, nkf, unzip, pipenvをインストール
```
apt-get -y update
apt-get -y upgrade
apt-get -y install cmake libpq-dev nkf unzip 
pip -q install pipenv
```
### 4.2 .envファイルを更新
開発環境、本番環境ともに, .envファイルは書き換えた後プロジェクトディレクトリの下にコピー(複製)をする.(pipenvが環境変数を読み込むため)
```
project_dir/.env
```
#### 開発環境
+ `.env`を書き換える
  + **(must)**`SECRET_KEY`をランダムな値に設定(50文字以上)
  + **(must)**`COMMENT_REPOSITORY_URL`を再設定する
    + [mimosa-project/emwiki-contents](https://github.com/mimosa-project/emwiki-contents)をForkしたレポジトリのURLに書き換える
  + その他の変更は、原則必要なし
+ `.env.db`を、必要に応じて書き換える
  + 変更は、原則必要なし
#### 本番環境
+ `.env`を書き換える
  + **(must)**`DEBUG=False`に設定
  + **(must)**`SECRET_KEY`をランダムな値に設定(50文字以上)
  + **(must)**`DJANGO_ALLOWED_HOSTS`を、デプロイするホストに設定
  + **(must)**`COMMENT_REPOSITORY_URL`を再設定
  + **(must)**`COMMENT_COMMIT_BRANCH`を`mml_commented`に設定
  + **(must)**`SQL_USER`を再設定
  + **(must)**`SQL_PASSWORD`を再設定
  + **(must)**`MIZAR_VERSION`を再設定
  + その他の設定を適宜再設定
+ `.env.db`を書き換える
  + **(must)**`.env`に設定した`SQL_USER`の値を`POSTGRES_USER`に設定
  + **(must)**`.env`に設定した`SQL_PASSWORD`の値を`POSTGRES_PASSWORD`に設定
+ `docker-compose.yml`内のhttps-portalを変更
  + **(must)**`DOMAINS: 'localhost->http://nginx:8000'`の`localhost`を、デプロイするドメインに変更
  + **(must)**`STAGE: 'production'`をコメントから外す

### 4.3コンテナの作成
#### 開発環境
+ 必要ファイルは`.devcontainer`の中にある
+ VSCodeの拡張機能`ms-vscode-remote.remote-containers`を用いることで簡単に行うことができる
+ 時間がかかる点に注意
```
cd .devcontainer
docker-compose up -d
```
#### 本番環境
+ 必要ファイルは`.prodcontainer`の中にある
+ 時間がかかる点に注意
+ 実行後、20分程度待つ
```
cd .prodcontainer
docker-compose up -d --build
```

### 4.4 必要ファイルの追加
+ 開発環境、本番環境の、いずれかの方法でファイルを追加する
+ 最後に確認事項を読み、ファイルの存在を確認する
  + なければ手動で追加する際の注意点を参考に、手動でファイルを追加する

#### 開発環境
+ プロジェクトのルートディレクトリに戻り`initialize.sh`をsudoで実行する(初回のみ)
```
cd ..
sudo sh initialize.sh dev
```

#### 本番環境
+ 本番環境ではコンテナ作成時に自動で`sh initialize.sh prod`が実行されるので特に操作は必要なし

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
  + `project_dir/emwiki/search/data`

#### initialize.shについて
+ initialize.shを実行すると初期設定が行われます. 具体的には以下の処理が行われます. 設定を変更したい場合はinitialize.shを書き換えてください
  + emwikiで使用するMizarファイル等を自動でダウンロードし, 解凍, 文字コードの変換, 敵切な場所への配置を行います<br>
  + emparserがcloneされます
  + .envファイルに記述した`COMMENT_REPOSITORY_URL`の`COMMENT_COMMIT_BRANCH`のブランチからemwiki-contentsがcloneされます
  + キャッシュテーブルの作成と, マイグレーションが行われます
  + ダウンロードしたMizarファイル等からemwikiの実行に必要なファイルが生成されます
+ initialize.shを実行したときに、Mizarファイルが既に存在する場合はエラーが出力され、Mizarファイルがダウンロードされません
```
sudo sh initialize.sh dev
Loaded environment from .devcontainer/.env
abstr files already exists
```
+ rmオプションをつけて、initialize.shを実行すると既に存在するMizarファイルを削除できます. 上記のエラーが出た場合はこの操作を行ってください.
```
sudo sh initialize.sh rm
```

#### 独自コマンドについて
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

### 4.5 実行
#### 開発環境
+ pipenvの仮想環境に入る
```
pipenv shell
```
+ superuserの作成
```
cd emwiki
python manage.py createsuperuser
```
+ 実行
```
python manage.py runserver
```
#### 本番環境
+ superuserの作成
```
docker-compose exec python pipenv run python /workspace/emwiki/manage.py createsuperuser
```
+ 実行
```
docker-compose exec python pipenv run python /workspace/emwiki/manage.py runserver
```
### 4.6 終了
```
docker-compose down
```
### 4.7 永続化データ
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

