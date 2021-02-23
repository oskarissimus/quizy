from collections import UserDict
import requests


class CategoryDict(UserDict):
    @classmethod
    def fromopentdbapi(cls):
        d = cls()
        r = requests.get('https://opentdb.com/api_category.php')
        for c in r.json()['trivia_categories']:
            d[c['id']]=c['name']
        return d

    def to_choice_field_choices(self):
        return list(self.items())
