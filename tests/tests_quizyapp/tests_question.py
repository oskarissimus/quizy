from django.test import TestCase
from quizyapp.question import QuestionList
from .test_mocks import mock_default, mock_category, raw_question_list
import responses

class QuestionListTests(TestCase):

    @responses.activate
    def test_retreiving_data_from_opentdb_api(self):
        responses.add(**mock_category)
        responses.add(**mock_default)
        rql = QuestionList.get_raw_question_list_from_opentdb_api()
        self.assertEqual(rql, raw_question_list)

    @responses.activate
    def test_invalid_category_before_retreiving_question_list_raises_value_error(self):
        with self.assertRaises(ValueError):
            QuestionList.get_raw_question_list_from_opentdb_api(category=39)

    @responses.activate
    def test_invalid_difficulty_before_retreiving_question_list_raises_value_error(self):
        with self.assertRaises(ValueError):
            QuestionList.get_raw_question_list_from_opentdb_api(difficulty='very hard')
