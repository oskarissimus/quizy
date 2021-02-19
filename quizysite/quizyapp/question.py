from collections import UserList
from .category import CategoryDict
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
        answers = [question_json['correct_answer']]
        answers += question_json['incorrect_answers']
        return cls(
            question_text=question_json['question'],
            answers=answers,
            correct_answer=question_json['correct_answer']
        )


    def get_answers_as_choice_field_choices(self):
        ret = []
        for answer in self.answers:
            ret.append((answer,answer))
        return ret

class QuestionList(UserList):

    @staticmethod
    def get_raw_question_list_from_opentdb_api(
        amount=3, category=9, difficulty='easy') -> List:
        
        if category not in CategoryDict.fromopentdbapi().keys():
            raise ValueError(f'category {category} does not exist')

        params = {
            'amount':     amount,
            'category':   category,
            'difficulty': difficulty
            }

        url    = 'https://opentdb.com/api.php'
        
        
        r = requests.get(url,params=params)
        return r.json()['results']

    @classmethod
    def fromopentdbapi(cls, amount=3, category=9, difficulty='easy') -> List[Question]:
        raw_question_list = \
            cls.get_raw_question_list_from_opentdb_api(
                amount=amount,
                category=category,
                difficulty=difficulty)

        l = cls()
        for raw_question in raw_question_list:
            l.append(Question.fromopentdbapiformat(raw_question))

        return l
