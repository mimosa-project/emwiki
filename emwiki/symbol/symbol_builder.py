from symbol.models import Symbol
from symbol.symbol_maker.processor import Processor

from django.conf import settings


class SymbolBuilder:
    from_dir = settings.MML_HTML_DIR

    def __init__(self):
        self.objects = []

    def delete_models(self):
        Symbol.objects.all().delete()
        print('Deleted all Symbols')

    def create_models(self):
        processor = Processor()
        processor.read(self.from_dir)
        processor.compose()
        symbols = []
        for content in processor.contents:
            symbol = Symbol(name=content.symbol,
                            filename=content.filename(), type=content.type)
            symbols.append(symbol)
        Symbol.objects.bulk_create(symbols)
        print('Created Symbols')
