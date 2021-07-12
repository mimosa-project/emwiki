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
            miz_files = glob.glob("*.miz")  # mmlディレクトリの.mizファイルを取り出す

        finally:
            os.chdir(cwd)

        article2references = retrieve_dependency.make_miz_dependency()
        self.assertEqual(len(miz_files), len(article2references))
