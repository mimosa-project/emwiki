from contents.contents.scripts.content_builder import ContentBuilder
from contents.symbol.scripts.builder.processor import Processor


class SymbolBuilder(ContentBuilder):

    def __init__(self):
        self.processor = Processor()

    def bulk_build(self, raw_htmlizedmml_dir, product_symbolhtml_dir):
        self.processor.execute(raw_htmlizedmml_dir, product_symbolhtml_dir)
