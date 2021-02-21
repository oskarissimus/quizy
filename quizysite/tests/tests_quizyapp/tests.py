from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from django.urls import reverse
from quizyapp.question import Question, QuestionList
import responses
import requests
import json
from quizyapp.test_mocks import mock_amount_2, mock_default, raw_question_list, mock_category, mock_art_category
from quizyapp.views import quiz
from quizyapp.category import CategoryDict
# Create your tests here.




class CategoryDictTests(TestCase):
    def setUp(self) -> None:
        responses.add(**mock_category)
        return super().setUp()

    @responses.activate  
    def test_building_category_list_from_opentdb_api(self):
        cl = CategoryDict.fromopentdbapi()
        self.assertEqual(cl[29],'Entertainment: Comics')