## 環境構築
- `README.md`に記載されているようにVScodeの`ターミナル→タスクの実行→Setup`を実行すると環境構築が行われます．
- 実行されるタスクは`.vscode/tasks.json`で定義されています．
- `.vscode/tasks.json`で実行されるスクリプトは`scripts`に置かれています．
- Setupが途中で失敗した場合，問題を解消し，失敗したタスクから順に実行し直すことで，環境構築を続きから行うことができます．
- 環境構築後，f5(デバックの開始)でサーバを起動します．または`pipenv shell`で仮想環境に入り，`python emwiki/manage.py runserver`を実行することで起動できます．

### Setupタスクで実行されるタスクの説明
1. `Install packages`: 必要なパッケージのインストールをします．パッケージを追加した場合は`scripts/install-packages.sh`に追記してください．
2. `Clone emwiki-contents`: emwiki-contentsをクローンします．emwiki-contentsディレクトリが既にありエラーが発生し場合，ディレクトリを削除し，再実行するか，このタスクをスキップしてください．emwiki-contentsはArticleのコメントを管理するリポジトリで，中身はコメントが埋め込まれたmizファイルです．詳しくは山道さんの論文を参照してください．
3. `Decompress mmlfiles`: emwikiで使用するmmlのデータを解凍します．mmlfilesの説明は[こちら](#mmlfiles)．
4. `Build mizcore`: mizcoreをビルドします．
5. `Install python packages`:
6. `install node packages`:
7. `Create services for development`: デフォルトでは`wsl + dbコンテナ`での開発を想定しています．Dockerコンテナ上で開発を行う場合は`Dockerfile`と`docker-compose.yml`を適宜変更してください．Dockerコンテナ上で開発を行う場合は，以下のことに気をつけて下さい．
   - メモリを大量に消費する
   - バインドを設定していない場合，コンテナ内の変更はローカルのファイルに反映されない．
8. `Migrate`: マイグレーションファイルをもとにマイグレーションを実行します．上手く実行されない場合は，`python manage.py makemigrations article`のように一つずつアプリを指定して実行してください．
9. `Load article data to database`: 管理コマンド[load_articles](#load_articles)が実行されます．
10. `Load symbol data to database`: 管理コマンド[load_symbols](#load_symbols)が実行されます．

## mmlfiles
以下のファイルは別リポジトリ([emwiki-mmlfiles](https://github.com/mimosa-project/emwiki-mmlfiles))で管理しています．
- abs，bib，miz，vctファイル
- HTMLized MML
- symbolアプリのHTML
- searchアプリのindexデータ
- graphアプリの描画用データ

これらのデータはサイズが大きく，生成に時間がかかるため，生成済みのデータを圧縮し，emwiki-mmlfilesで管理しています．

これらのファイルに変更があった場合，emwiki-mmlfilesの[README](https://github.com/mimosa-project/emwiki-mmlfiles#for-developers)を参考に，変更後のファイルを圧縮し，emwiki-mmlfilesのリポジトリにプルリクエストを作成してください．

## Djangoの管理コマンド
### article
#### build_htmlizedmml
HTMLized MMLを生成するコマンドです．HTMLized MMLに変更を行った場合，このコマンドを実行して変更を反映してください．
#### load_articles
emwiki-contentsのmizファイルを解析し，aricleとcommentのオブジェクトを作成し，dbに登録します．
### symbol
#### build_mmlreference
symbolアプリのHTMLを生成するコマンドです．symbolアプリのHTMLに変更を行った場合，このコマンドを実行して変更を反映してください．
#### load_symbols
HTMLized MMLを解析し，symbolのオブジェクトを作成し，dbに登録します．
### search
#### build_search_data
searchアプリのindexデータを生成するコマンドです．
### graph
#### build_graph
graphアプリの描画用データを生成するコマンドです．

## プルリクエスト
プルリクエスト時には，Github Actionsで以下のテストが行われます.
- Djangoのテスト
- Javascriptのコードスタイルチェック
- Pythonのコードスタイルチェック

Github Actionsで行われる処理の手順は`.github/workflows/test.yml`に記述されています.

ローカル環境で同様のテストを実行するには，タスクの"PullRequest chec"を実行してください．

※pythonのテストが実行されない場合は，`python manage.py test`，または`python manage.py test {appname}`で実行できます．

## デプロイ
デプロイは[emwiki-deploy](https://github.com/mimosa-project/emwiki-deploy)で行います．デプロイ方法はREADMEを参照してください．emwikiの変更を更新する場合は，Releasesした後[How to update image](https://github.com/mimosa-project/emwiki-deploy#how-to-update-image)の操作のみを行ってください．
