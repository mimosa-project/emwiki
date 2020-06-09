from abc import ABCMeta, abstractmethod

from contents.article.scripts.article_initializer import ArticleInitializer
from contents.symbol.scripts.symbol_initializer import SymbolInitializer


class EmwikiInitializer:
    def __init__(self):
        self.article_initializer = ArticleInitializer()
        self.symbol_initializer = SymbolInitializer()

    def initialize(self):
        self.article_initializer.initialize()
        self.symbol_initializer.initialize()


class ContentInitializer(metaclass=ABCMeta):

    def initialize(self):
        self._generate_files()
        self._delete_models()
        self._create_models()

    @abstractmethod
    def _generate_files(self):
        pass

    @abstractmethod
    def _delete_models(self):
        pass

    @abstractmethod
    def _create_models(self):
        pass
