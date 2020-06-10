from abc import ABCMeta, abstractmethod
import os

from lxml import html


class File(metaclass=ABCMeta):
    def __init__(self, path):
        self.path = path

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self):
        pass


class MizFile(File):
    """.mizファイル

    入出力を担当
    """

    def __init__(self, path):
        super().__init__(path)
        self.text = None

    def read(self):
        with open(self.path, 'r') as f:
            self.text = f.read()

    def write(self):
        with open(self.path, 'w') as f:
            f.write(self.text)


class HtmlizedMmlFile(File):
    def __init__(self, path):
        super().__init__(path)
        self.root = None

    def read(self):
        self.root = html.parse(self.path)

    def write(self):
        text = html.tostring(self.root, pretty_print=True, encoding='utf-8').decode('utf-8')
        with open(self.path, mode='w') as f:
            f.write(text)
