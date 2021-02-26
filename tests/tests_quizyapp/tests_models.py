from hashlib import md5

import responses
from django.test import TestCase
from quizyapp.models import Answer, Category, Question

from .test_mocks import mock_category, mock_default
from quizyapp.category import init_category_list_from_api_if_none_available


class QuestionAndAnswerRelationTests(TestCase):
    def setUp(self):
        cat, created = Category.objects.get_or_create(id=9, name="General Knowledge")
        a = Answer.objects.create(text="A", is_correct=True)
        b = Answer.objects.create(text="B", is_correct=False)
        c = Answer.objects.create(text="C", is_correct=False)
        d = Answer.objects.create(text="D", is_correct=False)

        q = Question.objects.create(
            text="What is the first letter of alphabet?", category=cat, difficulty='easy')
        q.answers.add(a, b, c, d)

    def test_question_is_initialized(self):
        q = Question.objects.get(text="What is the first letter of alphabet?")
        self.assertEqual(q.text, "What is the first letter of alphabet?")

    def test_answers_are_initialized(self):
        q = Question.objects.get(text="What is the first letter of alphabet?")
        self.assertEqual(q.answers.get(text='A').text, 'A')

    def test_if_id_is_properly_initiated(self):
        hash_id = md5(''.join([
            "What is the first letter of alphabet?",
            "General Knowledge",
            "easy"
        ]).encode('utf-8')).hexdigest()
        q = Question.objects.get(id=hash_id)
        self.assertEqual(q.text, "What is the first letter of alphabet?")

    @responses.activate
    def test_question_is_properly_initialized_from_opentdb_api_format(self):
        responses.add(**mock_category)
        raw_question = {
            "category": "General Knowledge",
            "type": "multiple",
            "difficulty": "easy",
            "question": "pytanie",
            "correct_answer": "odp A",
            "incorrect_answers": [
                "odp B",
                "odp C"
            ]
        }

        q = Question.fromopentdbapiformat(raw_question)
        self.assertEqual(q.text, 'pytanie')


class CategoryModelTests(TestCase):
    @responses.activate
    def test_categories_are_properly_initiated_from_api_if_there_are_none(self):
        responses.add(**mock_category)
        init_category_list_from_api_if_none_available()
        c = Category.objects.get(name="General Knowledge")

        self.assertEqual(c.name, "General Knowledge")
        self.assertEqual(c.id, 9)
        self.assertEqual(Category.objects.get(id=15).name,
                         "Entertainment: Video Games")
