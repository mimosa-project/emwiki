from contents.article.scripts.article_initializer import ArticleInitializer
from contents.symbol.scripts.symbol_initializer import SymbolInitializer


class Initializer:
    def __init__(self):
        self.article_initializer = ArticleInitializer()
        self.symbol_initializer = SymbolInitializer()

    def initialize(self):
        self.article_initializer.initialize()
        self.symbol_initializer.initialize()
