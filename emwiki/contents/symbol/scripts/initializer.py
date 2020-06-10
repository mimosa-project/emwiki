import glob
import os
import urllib

from contents.contents.scripts.initializer import ContentInitializer
from contents.symbol.models import Symbol
from contents.symbol.scripts.builder import SymbolBuilder
from emwiki.settings import RAW_HTMLIZEDMML_DIR, PRODUCT_SYMBOLHTML_DIR


class SymbolInitializer(ContentInitializer):

    def __init__(self):
        self.builder = SymbolBuilder()
        self.raw_htmlizedmml_dir = RAW_HTMLIZEDMML_DIR
        self.product_symbolhtml_dir = PRODUCT_SYMBOLHTML_DIR

    def _generate_files(self):
        self.builder.bulk_build(self.raw_htmlizedmml_dir, self.product_symbolhtml_dir)

    def _delete_models(self):
        Symbol.objects.all().delete()

    def _create_models(self):
        symbols = []
        contents = self.builder.processor.contents
        for content in contents:
            path = os.path.join(self.product_symbolhtml_dir, content.filename())
            if os.path.isfile(path):
                symbol = Symbol(name=content.symbol, filename=content.filename())
                symbols.append(symbol)
            else:
                print(path)
                raise Exception
        Symbol.objects.bulk_create(symbols)
