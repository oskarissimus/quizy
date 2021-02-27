from typing import List
from django import forms
from .models import Answer, Category, Question


class MultipleQuestionsForm(forms.Form):
    def __init__(self, question_id_list: List[str], *args, **kwargs):
        super(MultipleQuestionsForm, self).__init__(*args, **kwargs)
        questions = Question.objects.in_bulk(question_id_list, field_name='id')
        self.fields = {id: forms.ChoiceField(
            widget=forms.RadioSelect,
            choices=Answer.objects.filter(question__id = id).values_list('id','text'),
            label=question.text) for id, question in questions.items()}


class QuizParamsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(QuizParamsForm, self).__init__(*args, **kwargs)
        self.fields['amount'] = forms.IntegerField(
            max_value=50, min_value=1, initial=3)
        # https://stackoverflow.com/questions/47600089/django-choicefield-cleaned-data-gets-string-instead-of-integer
        choices = Category.objects.values_list('id', 'name')
        # print(choices)
        self.fields['category'] = forms.TypedChoiceField(
            choices=choices, coerce=int)
        self.fields['difficulty'] = forms.ChoiceField(
            choices=Question.Difficulty.choices)
