from collections import UserList
import requests
from typing import List

class Question:
    '''
    helper class to easier build MultipleQuestionsForm
    '''
    def __init__(self, question_text:str, answers:List[str], correct_answer:str):
        self.question_text = question_text
        self.answers = answers
        self.correct_answer = correct_answer

    
    @classmethod
    def fromopentdbapiformat(cls, question_json):
        return cls(
            question_text='pytanie',
            answers=['odp A','odp B','odp C'],
            correct_answer='odp A')


    def get_answers_as_choice_field_choices(self):
        ret = []
        for answer in self.answers:
            ret.append((self.question_text,answer))
        return ret

class QuestionList(UserList):

    @staticmethod
    def get_raw_question_list_from_opentdb_api(
        amount=3, category=9, difficulty='easy') -> List:
        

        params = {
            'amount':     amount,
            'category':   category,
            'difficulty': difficulty
            }

        url    = 'https://opentdb.com/api.php'
        
        
        r = requests.get(url,params=params)
        return r.json()['results']

    # @classmethod
    # def fromopentdbapi(cls, )
