
from django.test import TestCase
from quizyapp.models import Question, Answer, Category


class QuestionAndAnswerRelationTests(TestCase):
    def setUp(self):
        cat = Category(id=9, name="general")
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
