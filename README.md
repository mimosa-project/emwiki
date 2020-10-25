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
  
  
![emwiki](https://user-images.githubusercontent.com/49423101/75423437-0c960400-5982-11ea-86e5-382c462a6fc7.png)

## 3 Requirement
written on [pipfile](https://github.com/mimosa-project/emwiki/blob/master/Pipfile)

## 4 Install
### 4.1 ホストの準備
update
```
sudo apt update
```
upgrade
```
sudo apt upgrade
```

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
  + **(must)**`COMMENT_REPOSITORY_URL`を再設定する(emwiki-contentsのURL)
  + その他は適宜変更する
+ `.devcontainer/.env.db`を、`.devcontainer/.env.db-sample`を元に新たに作成する
  + 適宜変更する
### 本番環境
+ `.env`を、`.env-sample`を元に新たに作成する
  + **(must)**`DEBUG=False`に設定
  + **(must)**`SECRET_KEY`をランダムな値に設定(50文字程度)
  + **(must)**`DJANGO_ALLOWED_HOSTS`を、デプロイするホストに設定
  + **(must)**`COMMENT_REPOSITORY_URL`を再設定する
  + **(must)**`COMMENT_PUSH_BRANCH`が`mml_commented`担っているかチェック
  + **(must)**`SQL_USER`を再設定する
  + **(must)**`SQL_PASSWORD`を再設定する
  + その他の設定を適宜再設定する
+ `.env.db`を、`.env.db-sample`を元に新たに作成する
  + **(must)**`.env`に設定した`SQL_USER`の値を`POSTGRES_USER`に設定
  + **(must)**`.env`に設定した`SQL_PASSWORD`の値を`POSTGRES_PASSWORD`に設定
+ `docker-compose.yml`内のhttps-portalを変更
  + **(must)**`DOMAINS: 'localhost->http://nginx:8000'`の`localhost`を、デプロイするドメインに変更する
  + **(must)**`STAGE: 'production'`をコメントから外す


### 4.3 必要ファイルの追加
+ MML, HTMLized MML ファイルを追加する．
+ **MML, HTMLized MML のMMLバージョンは必ず統一すること．**
+ **MMLをHP等からDownloadする際にはutf-8に変換を行うこと**
+ `initialize.sh`を実行する事で、必要ファイルのDLが完了する
  + 必ず先に`.devcontainer/.env`or`.env`を作成する
```
sh initialize.sh
```
+ 確認事項
  + 以下のディレクトリにMMLファイル、HTMLized MMLファイルがあることを確認する
  + `project_dir/emwiki/contents/mizarfiles/emwiki-contents/mml/{*.miz}`
  + `project_dir/emwiki/contents/mizarfiles/htmlized_mml/{*.html}`

### 4.4コンテナの作成
#### 開発環境
+ 必要ファイルは`.devcontainer`の中にある
+ VSCodeの`ms-vscode-remote.remote-containers`を用いることで簡単に行うことができる
```
cd .devcontainer
docker-compose up -d --build
```
コンテナ作成時のみ、以下をコンテナ内で実行
+ 以下のインタプリタを設定
  + VSCodeの場合は、コマンドパレットから、`python select interpreter`から設定できる
```
/usr/local/bin/python
```
+ superuserの作成
```
python manage.py createsuperuser
```
+ MML, HTMLizedMMLファイルの加工
```
python manage.py generate all
```
+ Article, Comment, Symbolの登録
```
python manage.py register all
```
コンテナ作成・起動後、実行方法は通常通り
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
### 4.6 終了
```
docker-compose down
```
### 4.7 永続化データ
dockerのvolumeに保管されている
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
### emwiki-contents
+ `mml`ブランチにcheckoutする
+ `/emwiki/contents/mizarfiles/emwiki-contents/mml`を新しいMMLと交換する
+ add, commit(commitメッセージにバージョン情報をつける)
+ `mml_commented`ブランチにcheckoutする
+ 新たな`mml`ブランチの変更を`mml_commented`ブランチにマージする
### HTMLized MML
+ [ここ](https://ftp.icm.edu.pl/packages/mizar/xmlmml/)からDL可能
+ emwiki-contentsのバージョンと統一させる
+ `project_dir/emwiki/contents/mizarfiles/htmlized_mml/{*.html}`に配置する
+ `initialize.sh`を書き換える

## 6 Buckup

## 7 Licence

![MIT License](https://github.com/mimosa-project/emwiki/blob/master/LICENSE)

