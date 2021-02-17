from django.test import TestCase, Client
from django.urls import reverse
from .question import Question, QuestionList
import responses
import json

# Create your tests here.

class ViewTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        return super().setUp()
    def test_quizy_url_returns_200(self):
        response = self.client.get(reverse('quiz'))
        self.assertEqual(response.status_code, 200)

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
                ('pytanie','odp A'),
                ('pytanie','odp B'),
                ('pytanie','odp C'),
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
        print(q.answers)
        assert q.answers        == ['odp A','odp B','odp C']
        assert q.correct_answer == 'odp A'

class QuestionListTests(TestCase):
    def setUp(self) -> None:
        self.raw_question_list = [
            {
                "category": "General Knowledge",
                "type": "boolean",
                "difficulty": "easy",
                "question": "The Great Wall of China is visible from the moon.",
                "correct_answer": "False",
                "incorrect_answers": [
                    "True"
                ]
            },
            {
                "category": "General Knowledge",
                "type": "boolean",
                "difficulty": "easy",
                "question": "A scientific study on peanuts in bars found traces of over 100 unique specimens of urine.",
                "correct_answer": "False",
                "incorrect_answers": [
                    "True"
                ]
            },
            {
                "category": "General Knowledge",
                "type": "multiple",
                "difficulty": "easy",
                "question": "Which country, not including Japan, has the most people of japanese decent?",
                "correct_answer": "Brazil",
                "incorrect_answers": [
                    "China",
                    "South Korea",
                    "United States of America"
                ]
            }
        ]
        responses.add(**{
        'method'         : responses.GET,
        'url'            : 'https://opentdb.com/api.php?amount=3&category=9&difficulty=easy',
        'body'           : json.dumps({"response_code":0,"results":self.raw_question_list}),
        'status'         : 200,
        'content_type'   : 'application/json',
        })

        return super().setUp()

    @responses.activate  
    def test_retreiving_data_from_opentdb_api(self):
        rql = QuestionList.get_raw_question_list_from_opentdb_api()
        assert rql == self.raw_question_list

    @responses.activate  
    def test_constructor_from_api(self):
        ql = QuestionList.fromopentdbapi()
        self.assertEqual(ql[0].question_text, "The Great Wall of China is visible from the moon.")
        self.assertEqual(ql[2].correct_answer,"Brazil")