from contents.contents.scripts.builder import ContentBuilder
from contents.symbol.scripts.build_processor.processor import Processor


class SymbolBuilder(ContentBuilder):

    def __init__(self):
        self.processor = Processor()

    def bulk_build(self, from_dir, to_dir):
        self.processor.execute(from_dir, to_dir)
