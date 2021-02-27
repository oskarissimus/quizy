from quizyapp.models import Category
from django.test import TestCase
from quizyapp.utils.category import init_category_list_from_api_if_none_available, get_category_dict_from_opentdb_api
import responses
from ..test_mocks import mock_category

class CategoryUtilsTests(TestCase):

    @responses.activate
    def test_get_category_dict_from_opentdb_api_retreives_categories(self):
        responses.add(**mock_category)
        category_dict = get_category_dict_from_opentdb_api()
        
        self.assertEqual(category_dict[9], "General Knowledge")
        self.assertEqual(category_dict[15], "Entertainment: Video Games")
        
    @responses.activate
    def test_categories_are_properly_initiated_from_api_if_there_are_none(self):
        responses.add(**mock_category)
        init_category_list_from_api_if_none_available()
        c = Category.objects.get(name="General Knowledge")

        self.assertEqual(c.name, "General Knowledge")
        self.assertEqual(c.id, 9)
        self.assertEqual(Category.objects.get(id=15).name,
                         "Entertainment: Video Games")

