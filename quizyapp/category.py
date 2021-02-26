
from .models import Category
import requests

def init_category_list_from_api_if_none_available():
    if not Category.objects.all().count():
        category_dict = get_category_dict_from_opentdb_api()
        for id, name in category_dict.items():
            Category.objects.create(id=id, name=name)

def get_category_dict_from_opentdb_api():
    d = {}
    r = requests.get('https://opentdb.com/api_category.php')
    for c in r.json()['trivia_categories']:
        d[c['id']] = c['name']
    return d