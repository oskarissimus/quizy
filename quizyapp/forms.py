from django import forms
from typing import List
from .models import Question, Category

class MultipleQuestionsForm(forms.Form):
    def __init__(self, question_id_list:List[str], *args, **kwargs):
        super(MultipleQuestionsForm, self).__init__(*args, **kwargs)
        for question_id in question_id_list:
            question = Question.objects.get(id=question_id)
            self.fields[question.id] = forms.ChoiceField(
                widget  = forms.RadioSelect,
                choices = question.get_answers_as_choice_field_choices(),
                label = question.text)


class QuizParamsForm(forms.Form):
    amount = forms.IntegerField( max_value=50, min_value=1 ,initial=3)
    #https://stackoverflow.com/questions/47600089/django-choicefield-cleaned-data-gets-string-instead-of-integer
    Category.init_category_list_from_api_if_none_available()
    choices = [(c.id,c.name) for c in Category.objects.all()]
    category = forms.TypedChoiceField(choices=choices, coerce=int)
    difficulty = forms.ChoiceField(choices=Question.Difficulty.choices)