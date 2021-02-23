from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
import responses
from .test_mocks import mock_amount_2, mock_default, mock_category, mock_art_category
from quizyapp.views import quiz_questions, quiz_params


class QuizQuestionsViewUnauthorisedUserTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.path='/quiz/questions/'
        responses.add(**mock_category)
        responses.add(**mock_default)
        responses.add(**mock_amount_2)
        responses.add(**mock_art_category)
        return super().setUp()

    @responses.activate
    def test_quizy_url_returns_302_for_unauthorised_user(self):
        response = self.client.get(path=self.path)
        self.assertEqual(response.status_code, 302)


class QuizQuestionsViewAuthorisedUserTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.path='/quiz/questions/'
        self.user = User.objects.create_user(
            username='oskar', email='oskar@example.com', password='top_secret')
        self.client.login(username='oskar', password='top_secret')
        responses.add(**mock_category)
        responses.add(**mock_default)
        responses.add(**mock_amount_2)
        responses.add(**mock_art_category)
        return super().setUp()

    @responses.activate
    def test_quiz_questions_throw_400_with_no_params_provided(self):
        response = self.client.get(path=self.path)
        self.assertEqual(response.status_code, 400)

    @responses.activate
    def test_quiz_question_amount_is_configurable_by_get_params(self):
        params = {'amount': 2, 'category': 9, 'difficulty': 'easy'}
        response = self.client.get(path=self.path, data=params)

        # by default quiz view displays 3 questions. here we explicitly want 2 of them, and not third
        self.assertContains(
            response, "The Great Wall of China is visible from the moon.")
        self.assertContains(
            response, "A scientific study on peanuts in bars found traces of over 100 unique specimens of urine.")
        self.assertNotContains(
            response, "Which country, not including Japan, has the most people of japanese decent?")

    @responses.activate
    def test_quiz_throw_400_with_invalid_amount_provided(self):
        params = {'amount': 'zxalkfh', 'category': 9, 'difficulty': 'easy'}
        response = self.client.get(path=self.path, data=params)
        self.assertEqual(response.status_code, 400)

    @responses.activate
    def test_quiz_question_category_is_configurable_by_get_params(self):
        params = {'amount': 3, 'category': 25, 'difficulty': 'easy'}
        response = self.client.get(path=self.path, data=params)

        self.assertContains(response, "Who painted the Sistine Chapel?")
        self.assertContains(response, "Who painted The Starry Night?")
        self.assertContains(
            response, "Which painting was not made by Vincent Van Gogh?")


class QuizParamsViewTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(
            username='oskar', email='oskar@example.com', password='top_secret')
        self.client.login(username='oskar', password='top_secret')
        self.path='/quiz/params/'
        responses.add(**mock_category)
        responses.add(**mock_default)
        responses.add(**mock_amount_2)
        responses.add(**mock_art_category)
        return super().setUp()

    def test_quizy_params_url_returns_200_for_authorised_user(self):
        response = self.client.get(path=self.path)
        self.assertEqual(response.status_code, 200)
