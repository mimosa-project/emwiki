import glob
import os
import shutil
from collections import OrderedDict

from django.conf import settings
from lxml import html
from tqdm import tqdm


class HtmlFile:
    """HTMLファイルの読み込み・書き込みを行う
    """

    def __init__(self, path):
        self.path = path
        self.root = None

    def read(self):
        self.root = html.parse(self.path)

    def write(self):
        text = html.tostring(self.root, pretty_print=True,
                             encoding='utf-8').decode('utf-8')
        with open(self.path, mode='w') as f:
            f.write(text)


class HtmlizedMmlBuilder:
    """HTMLized MMLをarticleアプリケーション用に書き換える

    Attributes:
        from_dir(os.path): Directory where HTMLized MML files for input.
        to_dir(os.path): Directory where generated HTML files for output.
    """
    from_dir = settings.MML_HTML_DIR
    to_dir = settings.PRODUCT_HTMLIZEDMML_DIR

    def create_files(self):
        """Create HTML files.
        """
        existing_files = glob.glob(os.path.join(self.to_dir, '*'))
        for file in existing_files:
            if os.path.isfile(file):
                os.remove(file)
            elif os.path.isdir(file):
                shutil.rmtree(file)
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
        """Convert head element

        Args:
            root (lxml.etree._ElementTree): root tree.

        Returns:
            lxml.etree._ElementTree: root tree.
        """
        # Remove head elements
        for node in root.xpath('//head/*'):
            parent = node.getparent()
            parent.remove(node)
        head = root.xpath('//head')[0]

        # Add head elements
        head_elements = OrderedDict()
        for element in head_elements.values():
            head.append(element)
        return root
