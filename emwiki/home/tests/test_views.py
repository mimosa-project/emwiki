from django.test import TestCase, Client
from django.urls import reverse


class HomeViewTest(TestCase):

    def test_response_status(self):
        client = Client()
        response = client.get(reverse('home:home'), follow=True)
        self.assertEqual(response.status_code, 200)
