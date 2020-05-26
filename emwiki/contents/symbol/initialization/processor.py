import glob
import os
import os.path
import time
from contents.symbol.initialization.reader import Reader
from contents.symbol.initialization.composer import Composer
from contents.symbol.initialization.writer import ContentWriter
from contents.symbol.initialization.elements.element import Element
from contents.symbol.initialization.models import SymbolInitializer
from natsort import humansorted
from contents.symbol.models import Symbol
from tqdm import tqdm


class Processor:
    def __init__(self):
        Element._total_num = 0
        self.elements = []
        self.contents = []

    def execute(self):
        from_dir = Symbol.get_original_dir()
        to_dir = Symbol.get_static_dir()

        Symbol.objects.all().delete()
        self.read(from_dir)
        self.compose()
        self.write(to_dir)

    def read(self, from_dir):
        htmls = glob.glob(from_dir + "/*.html")
        htmls = humansorted(htmls)
        print('reading')
        for html in tqdm(htmls):
            reader = Reader()
            reader.read(html)
            self.elements += reader.elements
            
    def compose(self):
        print("composing...")
        composer = Composer()
        composer.elements = self.elements
        composer.build()
        self.contents = composer.contents

    def write(self, to_dir):
        SymbolInitializer.create(self.contents)

        contents_dir = to_dir
        if not os.path.exists(contents_dir):
            time.sleep(0.01)
            os.mkdir(contents_dir)

        print('writing')
        for content in tqdm(self.contents):
            content_writer = ContentWriter()
            content_writer.content = content
            content_writer.write(contents_dir + '/' + content.filename())
