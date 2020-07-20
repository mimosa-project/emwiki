from contents.symbol.models import Symbol
from contents.symbol.symbol_maker.processor import Processor
from contents.contents.content_builder import ContentBuilder
from emwiki.settings import RAW_HTMLIZEDMML_DIR


class SymbolBuilder(ContentBuilder):
    from_dir = RAW_HTMLIZEDMML_DIR

    def delete_models(self):
        Symbol.objects.all().delete()
        print('Deleted all Symbols')

    def create_models(self):
        processor = Processor()
        processor.read(self.from_dir)
        processor.compose()
        symbols = []
        for content in processor.contents:
            symbol = Symbol(name=content.symbol, filename=content.filename())
            symbols.append(symbol)
        Symbol.objects.bulk_create(symbols)
        print(f'Created Symbols')
