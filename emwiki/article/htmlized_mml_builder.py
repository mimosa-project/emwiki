from collections import OrderedDict
import glob
import os
import shutil

from lxml import html
from tqdm import tqdm

from article.models import Article
from content.html_builder import HtmlBuilder
from content.html_file import HtmlFile
from emwiki.settings import RAW_HTMLIZEDMML_DIR, PRODUCT_HTMLIZEDMML_DIR


class HtmlizedMmlBuilder(HtmlBuilder):
    from_dir = RAW_HTMLIZEDMML_DIR
    to_dir = PRODUCT_HTMLIZEDMML_DIR

    def delete_files(self):
        if os.path.exists(self.to_dir):
            shutil.rmtree(self.to_dir)
        os.mkdir(self.to_dir)

    def create_files(self):
        html_paths = glob.glob(os.path.join(self.from_dir, "*.html"))
        if not os.path.exists(self.to_dir):
            os.mkdir(self.to_dir)
        for from_path in tqdm(html_paths, desc='Creating Htmlized MML'):
            basename = os.path.basename(from_path)
            to_path = os.path.join(self.to_dir, basename)
            raw_html_file = HtmlFile(from_path)
            raw_html_file.read()
            product_html_file = HtmlFile(to_path)
            product_html_file.root = self.convert_head(raw_html_file.root)
            product_html_file.write()
        print("Copying proofs...")
        shutil.copytree(
            os.path.join(self.from_dir, 'proofs'),
            os.path.join(self.to_dir, 'proofs')
        )
        print("Copying refs...")
        shutil.copytree(
            os.path.join(self.from_dir, 'refs'),
            os.path.join(self.to_dir, 'refs')
        )

    def convert_head(self, root):
        for node in root.xpath('//head/*'):
            parent = node.getparent()
            parent.remove(node)
        head = root.xpath('//head')[0]
        head_elements = OrderedDict()
        for element in head_elements.values():
            head.append(element)
        return root
