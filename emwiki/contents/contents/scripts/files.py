from abc import ABCMeta, abstractmethod
import codecs

from lxml import html


class File(metaclass=ABCMeta):
    def __init__(self, name, path):
        self.name = name
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

    def __init__(self, name, path):
        self.text = ''

    def read(self):
        with open(self.path, 'r') as f:
            self.text = f.read()

    def write(self):
        with open(self.path, 'w') as f:
            f.write(self.text)


class HtmlizedMmlFile(File):
    def __init__(self, name, path):
        self.root = None

    def read(self):
        self.root = html.parse(self.path)

    def write(self):
        text = html.tostring(self.root, pretty_print=True, encoding='utf-8').decode('utf-8')
        with open(self.path, 'w') as f:
            f.write(text)


class SymbolHtmlFile(File):
    def __init__(self, name, path):
        self.content = []

    def read(self):
        pass

    def write(self):
        with codecs.open(self.path, 'w', 'utf-8-sig') as fp:
            fp.write("<!DOCTYPE html>\n"
                     "<html lang='en'>\n")
            self.write_header(fp)
            self.write_body(fp)
            fp.write("</html>\n")

    def _write_header(self, fp):
        fp.write("<head>\n"
                 "<meta charset='UTF-8'>\n"
                 "<title>" + self.content.symbol + "</title>\n"
                 "</head>\n")

    def _write_body(self, fp):
        fp.write("<body>\n")
        self.content.write(fp)
        fp.write("</body>\n")
