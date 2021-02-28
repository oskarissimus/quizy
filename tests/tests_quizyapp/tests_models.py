from hashlib import md5
from django.contrib.auth.models import User
from django.db.models.query import QuerySet

import responses
from django.test import TestCase
from quizyapp.models import Answer, Category, Question, UserAnswer

from .test_mocks import mock_category, mock_default
from quizyapp.utils.category import init_category_list_from_api_if_none_available
from django.db.utils import IntegrityError


class QuestionTests(TestCase):
    @responses.activate
    def setUp(self):
        responses.add(**mock_category)
        init_category_list_from_api_if_none_available()
        cat = Category.objects.get(
            id=9, name="General Knowledge")
        q = Question.objects.create(
            text="What is the first letter of alphabet?", category=cat, difficulty='easy')

    def test_question_is_initialized(self):
        q = Question.objects.get(text="What is the first letter of alphabet?")
        self.assertEqual(q.text, "What is the first letter of alphabet?")

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

        category = Category.objects.get(name='General Knowledge')
        q = Question.fromopentdbformat(raw_question, category)
        self.assertEqual(q.text, 'pytanie')

    def test_question_cannot_be_duplicated(self):
        cat = Category.objects.get(
            id=9, name="General Knowledge")
        with self.assertRaises(IntegrityError):
            Question.objects.create(
                text="What is the first letter of alphabet?", category=cat, difficulty='easy')


class AnswerTests(TestCase):
    @responses.activate
    def setUp(self):
        responses.add(**mock_category)
        init_category_list_from_api_if_none_available()
        cat = Category.objects.get(
            id=9, name="General Knowledge")
        q = Question.objects.create(
            text="What is the first letter of alphabet?", category=cat, difficulty='easy')
        Answer.objects.create(question=q, text="A", is_correct=True)
        Answer.objects.create(question=q, text="B", is_correct=False)
        Answer.objects.create(question=q, text="C", is_correct=False)
        Answer.objects.create(question=q, text="D", is_correct=False)
        return super().setUp()

    def test_answers_are_initialized(self):
        answers = Answer.objects.filter(
            question__text="What is the first letter of alphabet?").order_by('text').values_list('text', 'is_correct')
        expected_answers = (
            ('A', True),
            ('B', False),
            ('C', False),
            ('D', False),
        )
        self.assertQuerysetEqual(answers, [repr(r) for r in expected_answers])

    def test_answer_cannot_be_duplicated(self):
        q = Question.objects.get(
            text="What is the first letter of alphabet?")
        with self.assertRaises(IntegrityError):
            Answer.objects.create(question=q, text="A", is_correct=True)


class UserAnswerTests(TestCase):
    fixtures = ['category', 'question', 'answer', 'user', 'useranswer']

    def setUp(self):
        self.user = User.objects.get(id=1)

    def test_user_answer_is_properly_initiated(self):
        question = Question.objects.get(id='50b84e54aff20b91e2e085c76dc91928')
        answer = Answer.objects.get(id=9)
        user_answer = UserAnswer.objects.create(user=self.user, question=question, answer=answer)

        self.assertEqual(user_answer.user.username,'q')
        self.assertEqual(user_answer.answer.text,'True')
        self.assertEqual(user_answer.question.text,'The mitochondria is the powerhouse of the cell.')

    def test_get_points_for_user_returns_proper_value(self):
        self.assertEqual(UserAnswer.get_points_for_user(self.user),2)

    def test_get_all_answers_no_for_user_returns_proper_value(self):
        self.assertEqual(UserAnswer.get_all_answers_no_for_user(self.user),3)

