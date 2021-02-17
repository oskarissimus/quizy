from django.test import TestCase, Client
from django.urls import reverse

# Create your tests here.

class ViewTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        return super().setUp()
    def test_quizy_url_returns_200(self):
        response = self.client.get(reverse('quiz'))
        self.assertEqual(response.status_code, 200)
