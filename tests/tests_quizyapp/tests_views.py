import responses
from django.test import Client, TestCase

from .test_mocks import mock_amount_2, mock_art_category


class QuizQuestionsViewTests(TestCase):
    fixtures = ['category', 'user']

    def setUp(self) -> None:
        self.path = '/quiz/questions/'
        return super().setUp()

    def test_url_redirects_to_login_for_unauthorised_user(self):
        client = Client()
        response = client.get(path=self.path)
        self.assertRedirects(response, f'/accounts/login/?next={self.path}')

    def test_quiz_questions_throw_400_with_no_params_provided(self):
        client = Client()
        client.login(username='q', password='q')
        response = client.get(path=self.path)
        self.assertEqual(response.status_code, 400)

    @responses.activate
    def test_quiz_question_amount_is_configurable_by_get_params(self):
        responses.add(**mock_amount_2)
        client = Client()
        client.login(username='q', password='q')
        params = {'amount': 2, 'category': 9, 'difficulty': 'easy'}
        response = client.get(path=self.path, data=params)

        # by default quiz view displays 3 questions. here we explicitly want 2 of them, and not third
        self.assertContains(
            response, "The Great Wall of China is visible from the moon.")
        self.assertContains(
            response, "A scientific study on peanuts in bars found traces of over 100 unique specimens of urine.")
        self.assertNotContains(
            response, "Which country, not including Japan, has the most people of japanese decent?")

    def test_quiz_throw_400_with_invalid_amount_provided(self):
        client = Client()
        client.login(username='q', password='q')
        params = {'amount': 'zxalkfh', 'category': 9, 'difficulty': 'easy'}
        response = client.get(path=self.path, data=params)
        self.assertEqual(response.status_code, 400)

    @responses.activate
    def test_quiz_question_category_is_configurable_by_get_params(self):
        responses.add(**mock_art_category)
        client = Client()
        client.login(username='q', password='q')
        params = {'amount': 3, 'category': 25, 'difficulty': 'easy'}
        response = client.get(path=self.path, data=params)

        self.assertContains(response, "Who painted the Sistine Chapel?")
        self.assertContains(response, "Who painted The Starry Night?")
        self.assertContains(
            response, "Which painting was not made by Vincent Van Gogh?")


class QuizParamsViewTests(TestCase):
    fixtures = ['category', 'user']

    def setUp(self) -> None:
        self.path = '/quiz/params/'
        return super().setUp()

    def test_quizy_params_url_returns_200_for_authorised_user(self):
        client = Client()
        client.login(username='q', password='q')
        response = client.get(path=self.path)
        self.assertEqual(response.status_code, 200)

    def test_url_redirects_to_login_for_unauthorised_user(self):
        client = Client()
        response = client.get(path=self.path)
        self.assertRedirects(response, f'/accounts/login/?next={self.path}')


class QuizResultsViewTests(TestCase):
    fixtures = ['category', 'user']

    def setUp(self) -> None:
        self.path = '/quiz/results/'
        return super().setUp()

    def test_quizy_results_url_returns_400_if_none_answers_provided(self):
        client = Client()
        client.login(username='q', password='q')
        response = client.post(path=self.path)
        self.assertEqual(response.status_code, 400)

    def test_url_redirects_to_login_for_unauthorised_user(self):
        client = Client()
        response = client.get(path=self.path)
        self.assertRedirects(response, f'/accounts/login/?next={self.path}')