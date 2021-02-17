from django.shortcuts import render
from django.shortcuts import HttpResponse
from .forms import QuestionForm
from .question import Question, QuestionList

# Create your views here.
def quiz(request):
    if request.method == 'GET':
        question_list = QuestionList.fromopentdbapi(amount=1, category=9, difficulty='easy')
        q=question_list[0]
        form = QuestionForm(choices=q.get_answers_as_choice_field_choices(), label=q.question_text)

        context={'form': form}


        return render(request,context=context,template_name='quizyapp/quiz_question.html')

    else:
        print(request.POST)
        return HttpResponse(f"udzielono odpowiedzi")