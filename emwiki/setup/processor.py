from setup.article.processor import Processor as ArticleProcessor
from setup.mmlfrontend.mmlfrontend.processor import Processor as SymbolProcessor
from emwiki.settings import MML_DIR, MML_ARTICLES_ORIGINAL_DIR, MML_SYMBOLS_DIR


class Processor:
    def __init__(self):
        pass

    def execute(self):
        articleprocessor = ArticleProcessor()
        articleprocessor.execute(MML_DIR)

        symbolprocessor = SymbolProcessor()
        symbolprocessor.execute(
            MML_ARTICLES_ORIGINAL_DIR,
            MML_SYMBOLS_DIR
        )
