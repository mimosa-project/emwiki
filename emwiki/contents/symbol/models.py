from contents.contents.models import Content
from emwiki.settings import STATIC_SYMBOLS_URL


class Symbol(Content):
    category = 'Symbol'
    color = '#F9C270'

    def get_static_url(self):
        return STATIC_SYMBOLS_URL + self.filename
