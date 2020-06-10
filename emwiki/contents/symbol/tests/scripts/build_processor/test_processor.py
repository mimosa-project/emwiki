import glob
import os
import shutil
from unittest import TestCase

from contents.symbol.scripts.build_processor.processor import Processor
from emwiki.settings import TEST_RAW_HTMLIZEDMML_DIR, TEST_PRODUCT_SYMBOLHTML_DIR


class TestProcessor(TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    @staticmethod
    def filter_by_type(elements, typename):
        return [e for e in elements if e.type() == typename]

    def test_read(self):
        from_dir = TEST_RAW_HTMLIZEDMML_DIR
        processor = Processor()
        processor.read(from_dir)

        self.assertEqual(36, len(self.filter_by_type(processor.elements, 'pred')))
        self.assertEqual(10, len(self.filter_by_type(processor.elements, 'struct')))
        self.assertEqual(40, len(self.filter_by_type(processor.elements, 'mode')))
        self.assertEqual(185, len(self.filter_by_type(processor.elements, 'func')))
        self.assertEqual(96, len(self.filter_by_type(processor.elements, 'attr')))
        self.assertEqual(279, len(self.filter_by_type(processor.elements, 'cluster')))

    def test_execute(self):
        symbolhtml_paths = glob.glob(os.path.join(TEST_PRODUCT_SYMBOLHTML_DIR, '*.html'))
        for path in symbolhtml_paths:
            os.remove(path)

        from_dir = TEST_RAW_HTMLIZEDMML_DIR
        to_dir = TEST_PRODUCT_SYMBOLHTML_DIR
        processor = Processor()
        processor.execute(from_dir, to_dir)
