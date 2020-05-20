from lxml import html
from collections import OrderedDict


class Content:
    def __init__(self):
        self.root = None
        self.text = None

    def read(self, from_dir):
        self.root = html.parse(from_dir)

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
        
    def write(self, to_dir):
        with open(to_dir, 'w') as f:
            f.write(self.text)
