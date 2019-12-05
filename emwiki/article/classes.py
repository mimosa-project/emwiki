import glob
import os
import textwrap
from emwiki.settings import BASE_DIR


class Article():
    TARGET_BLOCK = (
        "theorem",
        "definition",
        "registration",
        "scheme",
        "notation",
        "proof",
    )
    HTML_DIR = "static/mizar_html/"
    MML_DIR = "static/mml/"

    def __init__(self, name):
        self.name = name
        self.html_path = os.path.join(BASE_DIR, self.HTML_DIR, f"{name}.html")
        self.mml_path = os.path.join(BASE_DIR, self.HTML_DIR, f"{name}.miz")

    @classmethod
    def all_names(cls):
        absolute_path_list = glob.glob(os.path.join(BASE_DIR, cls.MML_DIR, f"*.miz"))
        basename_list = [os.path.basename(absolute_path) for absolute_path in absolute_path_list]
        name_tuple = tuple([os.path.splitext(extention_name)[0] for extention_name in basename_list])
        return name_tuple

    @classmethod
    def all(cls):
        Article_tuple = tuple([Article(name) for name in cls.all_names()])
        return Article_tuple

    def exist(self):
        return self.name in self.all_names()

    def miz(self):
        with open(self.mml_path, "r") as f:
            return f.read()

    def embed(self):
        pass

    def extract(self):
        pass

    def comments(self):
        pass

    def comment(self, block, number):
        pass


class Comment():
    HEADER = "::: "
    LINE_MAX_LENGTH = 75
    COMMENT_DIR = "article/data/comment/"

    def __init__(self, article_name, block, order, text):
        self.article_name = article_name
        self.block = block
        self.order = order
        self.text = text

    def save(self):
        if not os.path.exists(os.path.join(BASE_DIR, self.COMMENT_DIR, self.article_name)):
            os.mkdir(os.path.exists(os.path.join(BASE_DIR, self.COMMENT_DIR, self.article_name)))
        if not self.text == "":
            with open(os.path.join(BASE_DIR, self.COMMENT_DIR, self.article_name, f'{self.block}_{self.order}'), 'w') as f:
                f.write(self.text)

    def format_text(self):
        comment_lines = []
        for line in self.text.splitlines():
            for cut_line in textwrap.wrap(line, self.LINE_MAX_LENGTH):
                comment_lines.append(f'{self.COMMENT_HEADER}{cut_line}')
        return '\n'.join(comment_lines)
