import os
import shutil
from symbol.models import Symbol
from symbol.symbol_maker.processor import Processor

from django.conf import settings


class SymbolHtmlBuilder:
    from_dir = settings.MML_HTML_DIR
    to_dir = Symbol.get_htmlfile_dir()

    def delete_files(self):
        if os.path.exists(self.to_dir):
            shutil.rmtree(self.to_dir)
        os.mkdir(self.to_dir)

    def create_files(self):
        print('Building Files')
        print(f'    from {self.from_dir}')
        print(f'    to   {self.to_dir}')
        processor = Processor()
        processor.execute(self.from_dir, self.to_dir)
