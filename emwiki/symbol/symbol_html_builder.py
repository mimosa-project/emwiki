import glob
import os

from symbol.models import Symbol
from symbol.symbol_maker.processor import Processor

from django.conf import settings


class SymbolHtmlBuilder:
    """Create symbol HTML files from HTMLized MML.
    """
    from_dir = settings.MML_HTML_DIR
    to_dir = Symbol.get_htmlfile_dir()

    def update_files(self):
        existing_files = glob.glob(os.path.join(self.to_dir, '*'))
        for file in existing_files:
            os.remove(file)
        print('Building Files')
        print(f'    from {self.from_dir}')
        print(f'    to   {self.to_dir}')
        processor = Processor()
        processor.execute(self.from_dir, self.to_dir)
