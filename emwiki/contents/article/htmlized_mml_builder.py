from collections import OrderedDict
import glob
import os
import shutil

from lxml import html
from tqdm import tqdm

from contents.article.models import Article
from contents.contents.html_builder import HtmlBuilder
from contents.contents.html_file import HtmlFile
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
        print(f'Building Files')
        print(f'    from {self.from_dir}')
        print(f'    to   {self.to_dir}')
        for from_path in tqdm(html_paths):
            basename = os.path.basename(from_path)
            to_path = os.path.join(self.to_dir, basename)
            raw_html_file = HtmlFile(from_path)
            raw_html_file.read()
            product_html_file = HtmlFile(to_path)
            product_html_file.root = self.convert_head(raw_html_file.root)
            product_html_file.write()

    def convert_head(self, root):
        for node in root.xpath('//head/*'):
            parent = node.getparent()
            parent.remove(node)
        head = root.xpath('//head')[0]
        head_elements = OrderedDict()
        head_elements['base'] = html.Element('base', href='/static/mml_articles/', target='_self')
        head_elements['mathjax_config'] = html.Element('script', type="text/javascript", src="/static/article/JavaScript/mathjax.js")
        head_elements['mathjax_for_IE11'] = html.Element('script', src="https://polyfill.io/v3/polyfill.min.js?features=es6")
        head_elements['mathjax'] = html.Element('script', id="MathJax-script", src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js", type="text/javascript")
        head_elements['iframe_css'] = html.Element('link', rel="stylesheet", href="/static/article/CSS/iframe.css", type="text/css")
        head_elements['iframe_js'] = html.Element('script', type="text/javascript", src="/static/article/JavaScript/iframe.js")
        for element in head_elements.values():
            head.append(element)
        return root
