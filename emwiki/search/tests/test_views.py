from django.test import TestCase, Client
from django.urls import reverse


class SearchTheoremViewTest(TestCase):

    def test_response_status(self):
        client = Client()
        response = client.get(reverse('search:index'), {'search_query': "j < i implies i -' (j + 1) + 1 = i -' j;"}, follow=True)
        self.assertEqual(response.status_code, 200)
