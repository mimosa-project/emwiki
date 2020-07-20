from lxml import html

from contents.contents.file import File


class HtmlFile(File):

    def __init__(self, path):
        super().__init__(path)
        self.root = None

    def read(self):
        self.root = html.parse(self.path)

    def write(self):
        text = html.tostring(self.root, pretty_print=True, encoding='utf-8').decode('utf-8')
        with open(self.path, mode='w') as f:
            f.write(text)
