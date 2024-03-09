from django.test import TestCase

from django.conf import settings
from search.theorem_searcher import TheoremSearcher


class TheoremSearcherTest(TestCase):
    def test_search(self):
        query_text = "let T be RelStr; attr T is Noetherian means the InternalRel of T is co-well_founded;"
        searcher = TheoremSearcher()
        search_results = searcher.search(query_text, 100, settings.TEST_SEARCH_INDEX_DIR)
        search_results = sorted(search_results, key=lambda x: x['relevance'], reverse=True)
        self.assertEqual(search_results[0]['label'], 'ABCMIZ_0:def1')
        self.assertEqual(len(search_results[0]), 6)
        self.assertEqual(len(search_results), 100)
