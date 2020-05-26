from contents.symbol.models import Symbol


class SymbolInitializer:
    def __init__(self):
        pass

    @classmethod
    def create(cls, contents):
        Symbol.objects.all().delete()
        symbols = []
        for content in self.contents:
            symbol = Symbol(
                name=content.symbol,
                filename=content.filename()
            )
            symbols.append(symbol)

        print(f'{len(symbols)} symbols were initialized')
        Symbol.objects.bulk_create(symbols)
