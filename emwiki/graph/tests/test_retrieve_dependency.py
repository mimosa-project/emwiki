
import glob
import os

from django.test import TestCase
from emwiki.settings import MML_MML_DIR
from graph import retrieve_dependency


class RetrieveDependencyTest(TestCase):
    def test_retrieve_dependency(self):
        cwd = os.getcwd()
        try:
            os.chdir(MML_MML_DIR)
            miz_files = glob.glob("*.miz")

        finally:
            os.chdir(cwd)

        article2references = retrieve_dependency.make_miz_dependency()
        # article数とノード数が一致するかを検証
        self.assertEqual(len(miz_files), len(article2references))
