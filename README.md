emwiki
====

Wiki for eco-Mizar

| Stage   | name        | address                               |
|---------|-------------|---------------------------------------|
| Release | application | https://em1.cs.shinshu-u.ac.jp/emwiki |
| Develop | application | http://localhost:8000/                |
|         | adminer     | http://localhost:8080/                |

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
+ Docker
+ VSCode

## 4 Install

Install docker
  - [Docker Desktop WSL 2 backend](https://docs.docker.com/docker-for-windows/wsl/)

Clone this repository with all submodules
```bash
$ git clone --recursive {repository url}
```

Create docker containers
```bash
$ docker compose up -d
```

Install VSCode
[Download Visual Studio Code](https://code.visualstudio.com/download)

Install Remote-Containers plugin to VSCode
- `ms-vscode-remote.remote-containers`
- ![image](https://user-images.githubusercontent.com/49423101/123077640-33205e00-d455-11eb-8aaa-2049b066d354.png)

Open folder in container using VSCode
- ![image](https://user-images.githubusercontent.com/49423101/123078181-af1aa600-d455-11eb-8a3e-a1e0bb40f509.png)

Install plugins reccomended at `.vscode/extenstions.json` to VSCode
- ![image](https://user-images.githubusercontent.com/49423101/123080809-4680f880-d458-11eb-86b3-e94706c4b7f2.png)


Select python interpreter
1. Use the `Python: Select Interpreter` command from the Command Palette (`Ctrl+Shift+P`)(Check `ms-python.python` plugin is installed if you can't find it)
    - ![select-interpreters-command](https://code.visualstudio.com/assets/docs/python/environments/select-interpreters-command.png)
1. Select python interpreter
- [Select and activate an environment](https://code.visualstudio.com/docs/python/environments#_select-and-activate-an-environment)
- ![image](https://user-images.githubusercontent.com/49423101/123081380-dc1c8800-d458-11eb-9bef-0c22ea86b929.png)

```bash
# run in emwiki-python-develop container
$ pwd
/emwiki

# Entry virtual environment
$ pipenv shell

# Migrate databse
$ python emwiki/manage.py migrate

# Build local files and load initial data
$ sh start.sh

# Create superuser
$ python manage.py createsuperuser
```

## 5 Runsever
```bash
$ python manage.py runserver
```
![image](https://user-images.githubusercontent.com/49423101/123082422-f3a84080-d459-11eb-99cd-38d29c176fd2.png)


## 6 Tasks
Some tasks can run as [Integrate with External Tools via Tasks](https://code.visualstudio.com/docs/editor/tasks)

![image](https://user-images.githubusercontent.com/49423101/123096671-4c7fd500-d46a-11eb-8a07-3f88aaae6ef9.png)
![image](https://user-images.githubusercontent.com/49423101/123096885-85b84500-d46a-11eb-93ca-764e75ec34fe.png)

### Test
```bash
$ pwd
/emwiki/emwiki
$ coverage run
```

### Check codestyle
```bash
$ pwd
/emwiki
$ flake8
```

### Coverage report
```bash
$ pwd
/emwiki/emwiki
$ coverage report
```

## 7 For Administrator
### To enable Build CI
Set secret variables
- Access "Settings" and "Secrets" on GitHub
- Set `DOCKER_USERNAME`
- Set `DOCKER_PASSWORD`
- If you set these variables, Build CI automatically push to your repository named `emwiki` with tag.

### How to publish Release or Prerelease
- Access "Releases" on GitHub
- Click "Draft new release"
  - Set tag version
  - If you want to release as beta, check "This is a pre-release"
- Click "Publish release"

### How to change Prerelease to Release
- Access "Releases" on GitHub
- Select prerelease you want to edit
- Click "Edit release"
  - Turn off "This is a pre-release"
- Click "Update release"


## 8 Appendix
### How to generate data for search theorem
+ 定理検索を使用するには`project_dir/emwiki/search/data/`内にabsファイルとvctファイルから生成されるデータが必要
+ データを生成するには`/emwiki/emwiki/mmlfiles/mml.vct`, `/emwiki/emwiki/mmlfiles/abstr/`が存在することを確認し、以下のコマンドを実行(実行に時間がかかります)
```bash
$ python manage.py generate_files search
```

### How to build local files
```bash
# Build HTMLized files
python manage.py build_htmlizedmml

# Build MML Reference files
python manage.py build_mmlreference

# Build search data
python manage.py build_search_data

# Build fmbibs
python manage.py build_fmbibs
```
### How to load models
```bash
# Load articles
python manage.py load_articles

# Load symbols
python manage.py load_symbols
```

### How to limit memory usage of WSL on your Windows

Create .wslconfig file at `C:\Users\{ username }\.wslconfig`

Add wsl2 configureration in `.wslconfig`(Change the value which you want)(See this [manual](https://docs.microsoft.com/en-us/windows/wsl/wsl-config#configure-global-options-with-wslconfig) for detail)
```
[wsl2]
memory=2GB
```

Restart WSL on PowerShell for apply the configuration.
```
$ wsl --shutdown
```

### How to limit memory usage of development container.

**この方法は現在非推奨で、将来サポートが打ち切られます。**

Add `services.python.deploy.resources.limits.memory` to `emwiki/ docker-compose.yml`
```yaml
services:
  python:
    build: .
    ~~~
    deploy:
      resources:
        limits:
          memory: 1G # Change this value which you want
    ~~~
...
```

Recreate python container.
Add `--compatibility` when you create development containers(because `deploy` can be used only version 2)
```Bash
docker-compose --compatibility up -d
```

## 9 Licence

![MIT License](https://github.com/mimosa-project/emwiki/blob/master/LICENSE)
