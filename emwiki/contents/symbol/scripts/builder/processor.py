import glob
import os
import urllib

from natsort import humansorted
from tqdm import tqdm

from .composer import Composer
from .elements.element import Element
from .reader import Reader
from .writer import Writer


class Processor:
    def __init__(self):
        Element._total_num = 0
        self.elements = []
        self.contents = []

    def execute(self, from_dir):
        self.read(from_dir)
        self.compose()
        self.write(to_dir)

    def read(self, from_dir):
        htmls = glob.glob(from_dir + "/*.html")
        htmls = humansorted(htmls)
        print('reading...')
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
        print("writing...")
        if not os.path.exists(to_dir):
            os.mkdir(to_dir)

        for content in tqdm(self.contents):
            writer = Writer()
            writer.content = content
            filename = urllib.parse.quote(content.symbol)
            writer.write(os.path.join(to_dir, filename)
