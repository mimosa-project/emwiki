from lxml import html
from collections import OrderedDict
from tqdm import tqdm
import os
import glob


class FileGenerator:
    def __init__(self):
        pass

    def generate(self, from_dir, to_dir):
        html_paths = glob.glob(os.path.join(from_dir, "*.html"))
        print(f'generating Files from {from_dir} to {to_dir}')
        for from_path in tqdm(html_paths):
            basename = os.path.basename(from_path)
            to_path = os.path.join(to_dir, basename)
            content = Content()
            content.read(from_path)
            content.build()
            content.write(to_path)


class Content:
    def __init__(self):
        self.root = None
        self.text = None

    def read(self, from_path):
        self.root = html.parse(from_path)

    def build(self):
        for node in self.root.xpath('//head/*'):
            parent = node.getparent()
            parent.remove(node)
        head = self.root.xpath('//head')[0]
        head_elements = OrderedDict()
        head_elements['base'] = html.Element('base', href='/contents/article/', target='_self')
        head_elements['mathjax_config'] = html.Element('script', type="text/javascript", src="/static/article/JavaScript/mathjax.js")
        head_elements['mathjax_for_IE11'] = html.Element('script', src="https://polyfill.io/v3/polyfill.min.js?features=es6")
        head_elements['mathjax'] = html.Element('script', id="MathJax-script", src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js", type="text/javascript")
        head_elements['iframe_css'] = html.Element('link', rel="stylesheet", href="/static/article/CSS/iframe.css", type="text/css")
        head_elements['iframe_js'] = html.Element('script', type="text/javascript", src="/static/article/JavaScript/iframe.js")
        for element in head_elements.values():
            head.append(element)
        self.text = html.tostring(self.root, pretty_print=True, encoding='utf-8').decode('utf-8')
        
    def write(self, to_path):
        with open(to_path, 'w') as f:
            f.write(self.text)
