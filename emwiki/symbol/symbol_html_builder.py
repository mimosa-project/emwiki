import os
import shutil

from content.html_builder import HtmlBuilder
from symbol.models import Symbol
from symbol.symbol_maker.processor import Processor
from emwiki.settings import RAW_HTMLIZEDMML_DIR


class SymbolHtmlBuilder(HtmlBuilder):
    from_dir = RAW_HTMLIZEDMML_DIR
    to_dir = Symbol.get_htmlfile_dir()

    def delete_files(self):
        if os.path.exists(self.to_dir):
            shutil.rmtree(self.to_dir)
        os.mkdir(self.to_dir)

    def create_files(self):
        print(f'Building Files')
        print(f'    from {self.from_dir}')
        print(f'    to   {self.to_dir}')
        processor = Processor()
        processor.execute(self.from_dir, self.to_dir)
