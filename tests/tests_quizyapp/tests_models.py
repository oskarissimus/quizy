from django.test import TestCase
from quizyapp.models import Question, Answer, Category
from hashlib import md5
from .test_mocks import mock_default, mock_category
import responses

class QuestionAndAnswerRelationTests(TestCase):
    def setUp(self):
        cat = Category(id=9, name="General Knowledge")
        cat.save()
        a = Answer(text="A", is_correct=True)
        b = Answer(text="B", is_correct=False)
        c = Answer(text="C", is_correct=False)
        d = Answer(text="D", is_correct=False)
        a.save()
        b.save()
        c.save()
        d.save()

        q = Question(text="What is the first letter of alphabet?", category=cat, difficulty='easy')
        q.save()
        q.answers.add(a,b,c,d)

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
        self.assertEqual(q.text , 'pytanie')

class CategoryModelTests(TestCase):
    @responses.activate
    def test_categories_are_properly_initiated_trom_api_if_there_are_none(self):
        responses.add(**mock_category)

        c = Category.get_or_init_category_list_from_api(category_name="General Knowledge")
        
        self.assertEqual(c.name, "General Knowledge")
        self.assertEqual(c.id, 9)
        self.assertEqual(Category.objects.get(id=15).name, "Entertainment: Video Games")