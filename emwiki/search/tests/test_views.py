from django.test import TestCase, Client
from django.urls import reverse


class SearchTheoremViewTest(TestCase):

    def test_response_status(self):
        client = Client()
        response = client.get(reverse('search:search_theorem'))
        self.assertEqual(response.status_code, 200)
