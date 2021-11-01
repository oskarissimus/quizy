import requests
from typing import List
from ..models import Category, Question

def get_raw_question_list_from_opentdb_api(
    amount=3, category=9, difficulty='easy') -> List:
    
    x = Category.objects.all()
    if not Category.objects.filter(id=category).exists():
        raise ValueError(f'category {category} does not exist')
    
    legal_difficulties = [c[0] for c in Question.Difficulty.choices]
    if difficulty not in legal_difficulties:
        raise ValueError(f'difficulty {difficulty} does not exist')

    params = {'amount': amount, 'category': category, 'difficulty': difficulty}
    url = 'https://opentdb.com/api.php'
    
    r = requests.get(url,params=params)
    return r.json()['results']
