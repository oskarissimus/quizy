from django import forms
from typing import List
from .question import Question
from .category import CategoryDict
from bootstrap4.widgets import RadioSelectButtonGroup

class QuestionForm(forms.Form):

    def __init__(self, choices, label, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields[label] = forms.ChoiceField(
            widget  = forms.RadioSelect,
            choices = choices)

class MultipleQuestionsForm(forms.Form):

    def __init__(self, questions:List[Question], *args, **kwargs):
        super(MultipleQuestionsForm, self).__init__(*args, **kwargs)
        for question in questions:
            self.fields[question.question_text] = forms.ChoiceField(
#                widget  = RadioSelectButtonGroup,
                widget  = forms.RadioSelect,
                choices = question.get_answers_as_choice_field_choices())

class QuizParamsForm(forms.Form):
    amount = forms.IntegerField( max_value=50, min_value=1 ,initial=3)
    category = forms.ChoiceField( choices=CategoryDict.fromopentdbapi().to_choice_field_choices() )
    difficulty = forms.ChoiceField( choices=(('easy','easy'),('medium','medium'),('hard','hard')) )