from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
import responses

from quizyapp.test_mocks import mock_amount_2, mock_default, mock_category, mock_art_category
from quizyapp.views import quiz, quiz_params
# Create your tests here.


class QuizViewTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='oskar', email='oskar@example.com', password='top_secret')
        responses.add(**mock_category)
        responses.add(**mock_default)
        responses.add(**mock_amount_2)
        responses.add(**mock_art_category)
        return super().setUp()

    def test_quizy_url_returns_200_for_authorised_user(self):
        request = self.factory.get(path=reverse('quiz'))
        request.user = self.user
        request.session = {}
        response = quiz(request)

        self.assertEqual(response.status_code, 200)

    @responses.activate
    def test_quizy_url_returns_302_for_unauthorised_user(self):

        response = self.client.get(reverse('quiz'))
        self.assertEqual(response.status_code, 302)

    @responses.activate
    def test_quiz_questions_show_up_for_authorised_user(self):
        # https://docs.djangoproject.com/en/3.1/topics/testing/advanced/

        # Create an instance of a GET request.
        request = self.factory.get('/quiz')

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user
        # manuallly set session, cuz i has to xD
        request.session = {}

        response = quiz(request)

        self.assertContains(
            response, "The Great Wall of China is visible from the moon.")
        self.assertContains(
            response, "A scientific study on peanuts in bars found traces of over 100 unique specimens of urine.")
        self.assertContains(
            response, "Which country, not including Japan, has the most people of japanese decent?")

    @responses.activate
    def test_quiz_question_amount_is_configurable_by_get_params(self):
        # tak się teraz zastanawiam czy to już jest test integracyjny czy jeszcze jednostkowy?

        params = {
            'amount':     2,
            'category':   9,
            'difficulty': 'easy'
        }

        request = self.factory.get(path=reverse('quiz'), data=params)
        request.user = self.user
        request.session = {}
        response = quiz(request)
        # by default quiz view displays 3 questions. here we explicitly want 2 of them, and not third
        self.assertContains(
            response, "The Great Wall of China is visible from the moon.")
        self.assertContains(
            response, "A scientific study on peanuts in bars found traces of over 100 unique specimens of urine.")
        self.assertNotContains(
            response, "Which country, not including Japan, has the most people of japanese decent?")

    @responses.activate
    def test_quiz_question_amount_is_3_when_non_int_amount_is_set(self):
        # tak się teraz zastanawiam czy to już jest test integracyjny czy jeszcze jednostkowy?

        params = {
            'amount':     'zxalkfh',
            'category':   9,
            'difficulty': 'easy'
        }

        request = self.factory.get(path=reverse('quiz'), data=params)
        request.user = self.user
        request.session = {}
        response = quiz(request)
        self.assertContains(
            response, "The Great Wall of China is visible from the moon.")
        self.assertContains(
            response, "A scientific study on peanuts in bars found traces of over 100 unique specimens of urine.")
        self.assertContains(
            response, "Which country, not including Japan, has the most people of japanese decent?")

    @responses.activate
    def test_quiz_question_category_is_configurable_by_get_params(self):
        # tak się teraz zastanawiam czy to już jest test integracyjny czy jeszcze jednostkowy?

        params = {
            'amount':     3,
            'category':   25,
            'difficulty': 'easy'
        }

        request = self.factory.get(path=reverse('quiz'), data=params)
        request.user = self.user
        request.session = {}
        response = quiz(request)
        self.assertContains(response, "Who painted the Sistine Chapel?")
        self.assertContains(response, "Who painted The Starry Night?")
        self.assertContains(
            response, "Which painting was not made by Vincent Van Gogh?")

    @responses.activate
    def test_quiz_question_category_is_9_when_non_int_category_is_set(self):
        # tak się teraz zastanawiam czy to już jest test integracyjny czy jeszcze jednostkowy?

        params = {
            'category':   'zxdfg',
        }

        request = self.factory.get(path=reverse('quiz'), data=params)
        request.user = self.user
        request.session = {}
        response = quiz(request)
        self.assertContains(
            response, "The Great Wall of China is visible from the moon.")
        self.assertContains(
            response, "A scientific study on peanuts in bars found traces of over 100 unique specimens of urine.")
        self.assertContains(
            response, "Which country, not including Japan, has the most people of japanese decent?")


class QuizParamsViewTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='oskar', email='oskar@example.com', password='top_secret')
        responses.add(**mock_category)
        responses.add(**mock_default)
        responses.add(**mock_amount_2)
        responses.add(**mock_art_category)
        return super().setUp()

    def test_quizy_params_url_returns_200_for_authorised_user(self):
        request = self.factory.get(path=reverse('quiz_params'))
        request.user = self.user
        request.session = {}
        response = quiz_params(request)
        self.assertEqual(response.status_code, 200)

# regression test to check if proper difficulty level