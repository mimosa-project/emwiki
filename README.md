emwiki
====

Wiki for eco-Mizar

| Stage   | name        | address                                       |
|---------|-------------|-----------------------------------------------|
| Release | application | https://em1.cs.shinshu-u.ac.jp/emwiki/release |
| Beta    | application | https://em1.cs.shinshu-u.ac.jp/emwiki/beta    |
| Develop | application | http://localhost:8000/                        |
|         | postgres    | http://localhost:5432/                        |
|         | adminer     | http://localhost:8080/                        |

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

1. Fork
    - Fork [mimosa-project/emwiki](https://github.com/mimosa-project/emwiki) to origin repository.
1. Clone this repository with all submodules.
    ```bash
    $ git clone --recursive {origin repository url}
    ```
1. Install VSCode
    - [Download Visual Studio Code](https://code.visualstudio.com/download)
1. Install Remote-Development plugin to VSCode
    - Open extensions (`Ctrl+Shift+X`) and search `ms-vscode-remote.vscode-remote-extensionpack` and install it.
1. Open cloned folder in WSL using Remote-Development plugin.
1. Install packages
    1. Update
        ```bash
        sudo apt-get update
        ```
    1. Upgrade
        ```bash
        sudo apt-get upgrade
        ```
    1. Install
        ```bash
        sudo apt-get -y install cmake libpq-dev python3-dev libssl-dev libffi-dev pbzip2 graphviz npm
        ```
1. Setup develop environment
    - Open the Command Palette (`Ctrl+Shift+P`) and select the `Tasks: Run Task` command and select the `Setup` command.
1. Create superuser
    - Open the Command Palette (`Ctrl+Shift+P`) and select the `Tasks: Run Task` command and select the `Create superuser` command and follow the instructions.

## 5 Runsever
Start debugging (`F5`).

## 6 Test
To check codestyle and test, open the Command Palette (`Ctrl+Shift+P`) and select the `Tasks: Run Test Task` command.

## 7 Tasks
See document for detail. [Integrate with External Tools via Tasks](https://code.visualstudio.com/docs/editor/tasks)

To run a task, open the Command Palette (`Ctrl+Shift+P`) and select the `Tasks: Run Task` command and select the task.

If you want to execute tasks manually in your terminal, definitions are witten on  `./vscode/tasks.json`.

## 8 For Administrator
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


## 9 Appendix

### 9.1 How to update Mizar version
[mmlfiles](https://github.com/mimosa-project/mmlfiles)

1. Update below files
    -  abstr/*.abs
    -  fmbibs/*.bib
    -  html/*.html
    -  mml/*.miz
    -  mml.ini
    -  mml.lar
    -  mml.vct
2. Build files
    - Open the Command Palette (`Ctrl+Shift+P`) and select the `Tasks: Run Task` command and select the `Build application staitc files` command.
3. Compress mmlfiles
    - Open the Command Palette (`Ctrl+Shift+P`) and select the `Tasks: Run Task` command and select the `Compress mmlfiles` command.
4. Commit  & Push & PullRequest

### 9.2 PR Checklist
- [ ] **Protect GitHub-flow**
- [ ] Execute [Test task](#6-test)
- [ ] Create PullRequest
    - [ ] Write title and each sections
    - [ ] Set Reviewers
    - [ ] Set Assignees
    - [ ] Set Labels
    - [ ] Set Linked issues
        - [プルリクエストをIssueにリンクする](https://docs.github.com/ja/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue)
- [ ] Check if CI has passed

## 10 Licence

![MIT License](https://github.com/mimosa-project/emwiki/blob/master/LICENSE)
