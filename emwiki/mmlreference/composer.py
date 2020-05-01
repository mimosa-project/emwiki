from bs4 import BeautifulSoup
import os
from emwiki.settings import BASE_DIR
import glob


class Composer():

    def __init__(self):
        self.contents = []
    
    def execute(self, from_dir, to_dir):
        self.read(from_dir)
        self.build()
        self.write(to_dir)

    def read(self, from_dir):
        mml_contents_paths = glob.glob(from_dir + "/*.html")
        mml_contents_paths_len = len(mml_contents_paths)
        for index, path in enumerate(mml_contents_paths):
            print(f'reading{index}/{mml_contents_paths_len}')
            content = Content()
            content.read(path)
            self.contents.append(content)

    def build(self):
        contents_len = len(self.contents)
        for index, content in enumerate(self.contents):
            print(f'building{index}/{contents_len}')
            content.translate()

    def write(self, to_dir):
        contents_len = len(self.contents)
        for index, content in enumerate(self.contents):
            print(f'writing{index}/{contents_len}')
            content.write(to_dir)


class Content():

    def __init__(self):
        self.soup = BeautifulSoup
        self.filename = ''
        self.type = ''
        self.symbol = ''

    def read(self, path):
        with open(path, 'r') as f:
            self.soup = BeautifulSoup(f, 'html.parser')
        self.type, self.symbol = \
            self.soup.select('div.mml-summary h1')[0].string.split(' ')
        self.filename = self.symbol

    def translate(self):
        soup = BeautifulSoup(
            """
            {% extends 'base.html' %}
            {% block content %}
            """, 'html.parser')
        soup.insert(1, self.soup.select('div.mml-summary')[0])
        for element in self.soup.select('div.mml-element'):
            soup.append(element)
        soup.append('{% endblock %}')
        print(soup.select('div.mml-summary h1')[0]['class'])
        self.soup = soup

    def write(self, dir):
        with open(os.path.join(dir, f'{self.filename}.html'), 'w') as f:
            f.write(str(self.soup))


if __name__ == '__main__':
    from_dir = os.path.join(BASE_DIR, 'mizarfiles', 'mml-contents-test')
    to_dir = os.path.join(BASE_DIR, 'mmlreference', 'templates', 'mmlreference', 'mml-contents')
    composer = Composer()
    composer.execute(from_dir, to_dir)
