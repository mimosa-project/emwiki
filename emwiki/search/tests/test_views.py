from django.test import TestCase, Client
from django.urls import reverse


class SearchViewTest(TestCase):

    def test_response_status(self):
        client = Client()
        response = client.get(reverse('search:search'))
        self.assertEqual(response.status_code, 200)


class GetKeywordsTest(TestCase):

    def test(self):
        pass
