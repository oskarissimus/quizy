import responses
from .test_mocks import mock_category
from quizyapp.category import CategoryDict
from django.test import TestCase

class CategoryDictTests(TestCase):
    def setUp(self) -> None:
        responses.add(**mock_category)
        return super().setUp()

    @responses.activate
    def test_building_category_list_from_opentdb_api(self):
        cl = CategoryDict.fromopentdbapi()
        self.assertEqual(cl[29], 'Entertainment: Comics')
