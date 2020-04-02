emwiki
====

Wiki for eco-Mizar

## Description
This Web application can write a TeX-format description in the Mizar Mathmatical Library (MML), and make the description follow the MML update. This Web application provides users with the function of adding, editing, and browsing description of MML on a Wiki format Web platform. If there is an update to the MML, link the description to the new MML by running the program on the server.

## Demo
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

## Requirement
written on pipfile
+ Python
+ Django

## Install 
### git clone
```
git clone https://github.com/mimosa-project/emwiki.git
```
### install Python
```
sudo apt install python3.7 python3.7-dev
```
### install pip3
```
sudo apt install python3-pip
```
### install pipenv
```
pip3 install pipenv
```
### install libpq-dev
```
sudo apt-get install libpq-dev
```
### sync pipenv
```
pipenv sync
```
### add MML and HTMLized MML files
add MML files
```
emwiki/mizarfiles/mml/<here>
```

add HTMLized MML files
```
emwiki/static/mizar-html/<here>
```
```
RUN curl https://ftp.icm.edu.pl/packages/mizar/xmlmml/html_abstr.5.33.1254.noproofs.tar.gz | tar xzv -C /code/tmp
mv html/* emwiki/static/mizar-html/
RUN curl https://ftp.icm.edu.pl/packages/mizar/system/current/mizar-8.1.09_5.57.1355-arm-linux.tar | tar xv -C /code/tmp
RUN tar zxf /code/tmp/mizshare.tar.gz -C /code/tmp
mv mml/* emwiki/mizarfiles/mml/
```
Like this
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
       |- mizar-html
          |- proofs
          |- refs
          |- abcmiz_1.html
          |- abcmiz_1.html
          |- ...
       |- optional

## 開発環境

## 本番環境

## Licence

![MIT License](https://github.com/mimosa-project/emwiki/blob/master/LICENSE)

