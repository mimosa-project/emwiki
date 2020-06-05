import glob
import os
import urllib

from contents.contents.scripts.content_initializer import ContentInitializer
from contents.symbol.models import Symbol
from contents.symbol.scripts.symbol_builder import SymbolBuilder
from emwiki.settings import RAW_HTMLIZEDMML_DIR, PRODUCT_SYMBOLHTML_DIR


class SymbolInitializer(ContentInitializer):

    def __init__(self):
        self.builder = SymbolBuilder()

    def _generate_files(self):
        self.builder.bulk_build(RAW_HTMLIZEDMML_DIR, PRODUCT_SYMBOLHTML_DIR)
        from_dir = Symbol.get_original_dir()
        contents = self.content_generator.generate(from_dir)
        
        to_dir = Symbol.get_static_dir()
        self.file_generator.generate(contents, to_dir)

        Symbol.objects.all().delete()
        symbols = self.model_generator.generate(contents)
        Symbol.objects.bulk_create(symbols)

    def _delete_models(self):
        Symbol.objects.all().delete()

    def _create_models(self):
        symbols = []
        html_paths = glob.glob(os.path.join(self.product_htmlizedmml_dir, "*.html"))
        for path in html_paths:
            basename = os.path.basename(path)
            name_encoded = os.path.splitext(basename)[0]
            name = urllib.parse.unquote(name_encoded)
            symbol = Symbol(name=name)
            symbols.append(symbol)
        Symbol.objects.bulk_create(symbols)
