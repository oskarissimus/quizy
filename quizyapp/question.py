from collections import UserList
import requests
from typing import List
from .models import Category, Question

class QuestionList(UserList):

    @staticmethod
    def get_raw_question_list_from_opentdb_api(
        amount=3, category=9, difficulty='easy') -> List:
        
        Category.init_category_list_from_api_if_none_available()
        category_dict = {c.id:c.name for c in Category.objects.all()}

        if category not in category_dict:
            raise ValueError(f'category {category} does not exist')
        
        legal_difficulties = [c[0] for c in Question.Difficulty.choices]
        if difficulty not in legal_difficulties:
            raise ValueError(f'difficulty {difficulty} does not exist')

        params = {'amount': amount, 'category': category, 'difficulty': difficulty}
        url = 'https://opentdb.com/api.php'
        
        r = requests.get(url,params=params)
        return r.json()['results']