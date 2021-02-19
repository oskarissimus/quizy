from collections import UserDict
import requests
from typing import List


class CategoryList(UserDict):
    @classmethod
    def fromopentdbapi(cls):
        d = cls()
        r = requests.get('https://opentdb.com/api_category.php')
        for c in r.json()['trivia_categories']:
            d[c['id']]=c['name']
        return d