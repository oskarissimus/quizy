from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from django.urls import reverse
from .question import Question, QuestionList
import responses
import requests
import json
from .test_mocks import mock_amount_2, mock_default, raw_question_list
from .views import quiz
# Create your tests here.


class ViewTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='oskar', email='oskar@example.com', password='top_secret')
        return super().setUp()

    def test_quizy_url_returns_200(self):
        response = self.client.get(reverse('quiz'))
        self.assertEqual(response.status_code, 200)
            


    @responses.activate
    def test_quiz_questions_doesnt_show_for_unauthorised_user(self):
        responses.add(**mock_default)
        response = self.client.get(reverse('quiz'))
        self.assertNotContains(response, 'The Great Wall of China is visible from the moon.')

    @responses.activate
    def test_quiz_questions_show_up_for_authorised_user(self):
        #https://docs.djangoproject.com/en/3.1/topics/testing/advanced/
        responses.add(**mock_default)

        # Create an instance of a GET request.
        request = self.factory.get('/quiz')

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user
        #manuallly set session, cuz i has to xD
        request.session = {}

        response = quiz(request)

        self.assertContains(response, "The Great Wall of China is visible from the moon.")
        self.assertContains(response, "A scientific study on peanuts in bars found traces of over 100 unique specimens of urine.")
        self.assertContains(response, "Which country, not including Japan, has the most people of japanese decent?")

        
    @responses.activate
    def test_quiz_question_amount_is_configurable_by_get_params(self):
        #tak się teraz zastanawiam czy to już jest test integracyjny czy jeszcze jednostkowy?
        responses.add(**mock_default)
        responses.add(**mock_amount_2)
        params = {
            'amount':     2,
            'category':   9,
            'difficulty': 'easy'
            }

        request = self.factory.get(path=reverse('quiz'), data=params)
        request.user = self.user
        request.session = {}
        response = quiz(request)
        #by default quiz view displays 3 questions. here we explicitly want 2 of them, and not third
        self.assertContains(response, "The Great Wall of China is visible from the moon.")
        self.assertContains(response, "A scientific study on peanuts in bars found traces of over 100 unique specimens of urine.")
        self.assertNotContains(response, "Which country, not including Japan, has the most people of japanese decent?")



    @responses.activate
    def test_quiz_question_amount_is_3_when_non_int_amount_is_set(self):
        #tak się teraz zastanawiam czy to już jest test integracyjny czy jeszcze jednostkowy?
        responses.add(**mock_default)
        responses.add(**mock_amount_2)
        params = {
            'amount':     'zxalkfh',
            'category':   9,
            'difficulty': 'easy'
            }

        request = self.factory.get(path=reverse('quiz'), data=params)
        request.user = self.user
        request.session = {}
        response = quiz(request)
        self.assertContains(response, "The Great Wall of China is visible from the moon.")
        self.assertContains(response, "A scientific study on peanuts in bars found traces of over 100 unique specimens of urine.")
        self.assertContains(response, "Which country, not including Japan, has the most people of japanese decent?")
        

class QuestionTests(TestCase):
    def setUp(self) -> None:
        self.q = Question(
            question_text='pytanie',
            answers=['odp A','odp B','odp C'],
            correct_answer='odp A')
        return super().setUp()

    def test_constructor(self):
        assert self.q.question_text  == 'pytanie'
        assert self.q.answers        == ['odp A','odp B','odp C']
        assert self.q.correct_answer == 'odp A'
    
    def test_convertion_to_form_choices(self):
        self.assertEqual(
            self.q.get_answers_as_choice_field_choices(),
            [
                ('odp A','odp A'),
                ('odp B','odp B'),
                ('odp C','odp C'),
            ] )

    def test_constructor_from_opentdb_api_format(self):
        raw_question = {
            "category": "General Knowledge",
            "type": "multiple",
            "difficulty": "easy",
            "question": "pytanie INNE",
            "correct_answer": "odp A",
            "incorrect_answers": [
                "odp B",
                "odp C"
            ]
        }
        q = Question.fromopentdbapiformat(raw_question)
        assert q.question_text  == 'pytanie INNE'
        #print(q.answers)
        assert q.answers        == ['odp A','odp B','odp C']
        assert q.correct_answer == 'odp A'

class QuestionListTests(TestCase):


    @responses.activate  
    def test_retreiving_data_from_opentdb_api(self):
        responses.add(**mock_default)
        rql = QuestionList.get_raw_question_list_from_opentdb_api()
        assert rql == raw_question_list

    @responses.activate  
    def test_constructor_from_api(self):
        responses.add(**mock_default)
        ql = QuestionList.fromopentdbapi()
        self.assertEqual(ql[0].question_text, "The Great Wall of China is visible from the moon.")
        self.assertEqual(ql[2].correct_answer,"Brazil")

