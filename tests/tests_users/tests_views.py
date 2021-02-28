from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls.base import reverse

class AuthenticatedUserViewTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(
            username='oskar', email='oskar@example.com', password='top_secret')
        self.client.login(username='oskar', password='top_secret')
        self.path='/register/'
        return super().setUp()

    def test_get_register_view_redirects_to_dashboard(self):
        response = self.client.get(self.path)
        self.assertRedirects(response,reverse("dashboard"))

class UnauthenticatedUserViewTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        return super().setUp()

    def test_view_response_code_200(self):
        paths = ('/register/', '/accounts/login/')
        for path in paths:
            with self.subTest(path=path):
                response = self.client.get(path=path)
                self.assertEqual(response.status_code, 200)
        
    def test_register_view_redirect_to_itsef_if_form_is_invalid(self):
        response = self.client.post(path='/register/')
        self.assertRedirects(response, '/register/')
    