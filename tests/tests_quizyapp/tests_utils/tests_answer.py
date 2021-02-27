from quizyapp.models import Answer, Category, Question
from django.test import TestCase
from quizyapp.utils.answer import get_or_create_answer_objects_from_opentdb_format


class AnswerUtilsTests(TestCase):

    def test_creating_answers_by_utility_function_works(self):
        raw_question = {
            "category": "General Knowledge",
            "type": "multiple",
            "difficulty": "easy",
            "question": "What is the first letter of alphabet?",
            "correct_answer": "A",
            "incorrect_answers": [
                "B",
                "C"
            ]
        }
        cat = Category.objects.create(id=9, name=raw_question['category'])
        text = raw_question['question']
        difficulty = raw_question['difficulty']
        question = Question.objects.create(
            text=text, category=cat, difficulty=difficulty)

        get_or_create_answer_objects_from_opentdb_format(
            raw_question=raw_question, question=question)

        self.assertEqual(Answer.objects.filter(question=question).count(), 3)
        answers = Answer.objects.filter(question=question).order_by(
            'text').values_list('text', 'is_correct')
        expected_answers = (
            ('A', True),
            ('B', False),
            ('C', False),
        )
        self.assertQuerysetEqual(answers, [repr(r) for r in expected_answers])
