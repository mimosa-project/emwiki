#!/bin/sh
# mkdir -p htmlized_mml
echo 'Downloading new HTMLized_MML'
# wget https://ftp.icm.edu.pl/packages/mizar/xmlmml/html_abstr.5.57.1355.tar.gz -O ./htmlized_mml/htmlized_mml.tar.gz
echo 'Extracting new HTMLized_MML'
# tar -zxf ./htmlized_mml/htmlized_mml.tar.gz -C htmlized_mml
echo 'Removing old HTMLized_MML'
# rm -r emwiki/contents/mizarfiles/htmlized_mml
echo 'Moving new HTMLized_MML'
# mv -i htmlized_mml/html emwiki/contents/mizarfiles/htmlized_mml
echo 'Remoing chaches'
# rm -r htmlized_mml

echo 'Cloning emwiki-contents'
git clone -b mml_commented https://github.com/etmula/emwiki-contents.git emwiki/contents/mizarfiles/emwiki-contents2
