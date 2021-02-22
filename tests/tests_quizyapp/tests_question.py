from django.test import TestCase
from quizyapp.question import Question, QuestionList
import responses
from quizyapp.test_mocks import mock_default, raw_question_list, mock_category


class QuestionTests(TestCase):
    def setUp(self) -> None:
        self.q = Question(
            question_text='pytanie',
            answers=['odp A', 'odp B', 'odp C'],
            correct_answer='odp A')
        return super().setUp()

    def test_constructor(self):
        assert self.q.question_text == 'pytanie'
        assert self.q.answers == ['odp A', 'odp B', 'odp C']
        assert self.q.correct_answer == 'odp A'

    def test_convertion_to_form_choices(self):
        self.assertEqual(
            self.q.get_answers_as_choice_field_choices(),
            [
                ('odp A', 'odp A'),
                ('odp B', 'odp B'),
                ('odp C', 'odp C'),
            ])

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
        assert q.question_text == 'pytanie INNE'
        # print(q.answers)
        assert q.answers == ['odp A', 'odp B', 'odp C']
        assert q.correct_answer == 'odp A'


class QuestionListTests(TestCase):

    def setUp(self) -> None:
        responses.add(**mock_category)
        responses.add(**mock_default)
        return super().setUp()

    @responses.activate
    def test_retreiving_data_from_opentdb_api(self):
        rql = QuestionList.get_raw_question_list_from_opentdb_api()
        assert rql == raw_question_list

    @responses.activate
    def test_constructor_from_api(self):
        ql = QuestionList.fromopentdbapi()
        self.assertEqual(ql[0].question_text,
                         "The Great Wall of China is visible from the moon.")
        self.assertEqual(ql[2].correct_answer, "Brazil")

    @responses.activate
    def test_invalid_category_before_retreiving_question_list_raises_value_error(self):
        with self.assertRaises(ValueError):
            QuestionList.get_raw_question_list_from_opentdb_api(category=39)
