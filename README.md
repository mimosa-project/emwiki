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

### sync pipenv
```
cd <piplock folder>
```
```
pipenv sync
```

### make local_settings.py
```
pipenv shell
```
```
cd emwiki/emwiki
```
```
python generate_secretkey_setting.py > local_settings.py
```

### add MML and HTMLized MML files
copy MML files
```
emwiki/static/mml/<here>
```

copy HTMLized MML files
```
emwiki/static/mizar-html/<here>
```

Like this

    emwiki
    |- accounts
    |- article
    |- emwiki
    |- static
       |- mml
          |- abcmiz_0.miz
          |- abcmiz_1.miz
          |- ...
       |- mizar-html
          |- proofs
          |- refs
          |- abcmiz_1.html
          |- abcmiz_1.html
          |- ...
       |- optional


## Licence

![MIT License](https://github.com/mimosa-project/emwiki/blob/master/LICENSE)

