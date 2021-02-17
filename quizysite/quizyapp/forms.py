from django import forms

class QuestionForm(forms.Form):

    def __init__(self, choices, label, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['answers_field'].choices = choices
        self.fields['answers_field'].label = label


    answers_field = forms.ChoiceField(widget=forms.RadioSelect)
