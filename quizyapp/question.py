from collections import UserList
from .category import CategoryDict
import requests
from typing import List
from html import unescape
import random
import json

class Question():
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
        answers = [unescape(a) for a in answers]
        question_text = unescape(question_json['question'])
        correct_answer = unescape(question_json['correct_answer'])
        return cls(
            question_text=question_text,
            answers=answers,
            correct_answer=correct_answer
        )

    @classmethod
    def from_dict(cls, question_dict):
        
        answers = question_dict['answers']
        question_text = question_dict['question_text']
        correct_answer = question_dict['correct_answer']
        return cls(
            question_text=question_text,
            answers=answers,
            correct_answer=correct_answer
        )

    def get_answers_as_choice_field_choices(self):
        ret = []
        for answer in self.answers:
            ret.append((answer,answer))
        return ret

    def to_dict(self):
        return self.__dict__

class QuestionList(UserList):

    @staticmethod
    def get_raw_question_list_from_opentdb_api(
        amount=3, category=9, difficulty='easy') -> List:
        
        category_dict = CategoryDict.fromopentdbapi()

        if category not in category_dict:
            raise ValueError(f'category {category} does not exist')

        params = {'amount': amount, 'category': category, 'difficulty': difficulty}
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
    def shuffle_answers(self):
        for question in self.data:
            random.shuffle(question.answers)
    
    def to_json(self):
        return json.dumps([question.to_dict() for question in self.data])

    @classmethod
    def from_json(cls, json_str):
        question_dict_list = json.loads(json_str)
        l = cls()
        for question_dict in question_dict_list:
            l.append(Question.from_dict(question_dict))
        return l