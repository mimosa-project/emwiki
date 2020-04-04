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
git clone
```
git clone https://github.com/mimosa-project/emwiki.git
```
install Python
```
sudo apt install python3.7 python3.7-dev
```
install pip3
```
sudo apt install python3-pip
```
install pipenv
```
pip3 install pipenv
```

### 4.2 必要ファイルの追加
+ MML, HTMLized MML ファイルを追加する．
+ **MML, HTMLized MML のMMLバージョンは必ず統一すること．**

MML
+ **文字コードがutf-8ではないファイルが存在する場合がある．**
  + 各自iconvなどのコマンドでutf-8に変換すること．
+ MMLファイルは[ここ](https://ftp.icm.edu.pl/packages/mizar/system/)からダウンロードできる．
```
emwiki/mizarfiles/mml/<here>
```

HTMLized MML
+ MMLファイルは[ここ](https://ftp.icm.edu.pl/packages/mizar/xmlmml/)からダウンロードできる．
```
emwiki/static/mizar-html/<here>
```

追加後，以下のようなディレクトリ構成とすること．
```
    emwiki
    |- accounts
    |- article
    |- emwiki
    |- mizarfiles
       |- mml
          |- abcmiz_0.miz
          |- abcmiz_1.miz
          |- ...
    |- static
       |- mizar_html
          |- proofs
          |- refs
          |- abcmiz_1.html
          |- abcmiz_1.html
          |- ...
       |- optional
```


## 4.3 開発環境
### 4.1 依存ライブラリのインストール手順

libpq-devをインストール(psycopg2のため)
```
sudo apt-get install libpq-dev
```
piplockを使用して，仮想環境にPythonの依存ライブラリをインストール
```
pipenv sync
```

### データベースの作成

Postgresデータベースを使用するため，dockerなどでpostgresデータベースを作成してください．



### .envの内容を変更

仮想環境に入る
```
pipenv shell
```

.envファイルを書き換える．postgresデータベースを利用するため，dockerなどでデータベースを作成後，下記のようにURLを.envでで指定してください．
```
SECRET_KEY={secret ramdom sting}
DATABASE_URL=postgresql://{user}:{password}@{IPaddress or hostname}:{port}/{dastabase}
```

migrate
```
python manage.py migrate
```

superuser作成
```
python manage.py createsuperuser
```
### 開発用サーバーの立ち上げ
仮想環境に入った状態で行ってください．
```
python manage.py runserver
```

## 4.4 本番環境

### 4.4.1 dockerのインストール

docker, docker-composeをインストール

### 4.4.2 .envファイルの変更
+ emwiki/.envファイルを，emwiki/.env.dockerファイルの内容に置きかえてください．
+ SECRET_KEY(英字50字)を書き換えてください．

### 4.4.3 起動
```
sudo docker-compose up --build -d
```
### 4.4.4 superuserの作成
```
sudo docker-compose run emwiki_python_1 pipenv run python manage.py createsuperuser
```
### 4.4.5 終了
```
sudo docker-compose down
```
### 4.4.6 生成物
DBデータはホスト側のemwiki/dockerpgsql-dataにあります．


## 5 Licence

![MIT License](https://github.com/mimosa-project/emwiki/blob/master/LICENSE)

