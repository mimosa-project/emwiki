from django.apps import AppConfig

from emwiki.settings import SYMBOL_DIR


class SymbolConfig(AppConfig):
    name = 'contents.symbol'
    path = SYMBOL_DIR
