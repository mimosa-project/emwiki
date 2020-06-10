from contents.article.scripts.initializer import ArticleInitializer
from contents.symbol.scripts.initializer import SymbolInitializer


class EmwikiInitializer:
    def __init__(self):
        self.article_initializer = ArticleInitializer()
        self.symbol_initializer = SymbolInitializer()

    def initialize(self):
        self.article_initializer.initialize()
        self.symbol_initializer.initialize()