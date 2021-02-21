from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from .forms import MultipleQuestionsForm, QuizParamsForm
from .question import Question, QuestionList
from django.contrib.auth.decorators import login_required
from .models import UserPoints
from django.views.generic import ListView
#from .category import CategoryList

# Create your views here.
@login_required
def quiz(request):
    if request.method == 'GET':
        
        amount = 3 # default value
        if 'amount' in request.GET and request.GET.get('amount').isdigit():
            amount = int(request.GET.get('amount'))

        category = 9 # default value
        if 'category' in request.GET and request.GET.get('category').isdigit():
            category = int(request.GET.get('category'))

        question_list = QuestionList.fromopentdbapi(amount=amount, category=category, difficulty='easy')
        question_list.shuffle_answers()
        form = MultipleQuestionsForm(question_list)

        skip_ceck = True
        if 'correct_answers_for_questions' not in request.session.keys() or skip_ceck:
            request.session['correct_answers_for_questions'] = {}

        for question in question_list:
            request.session['correct_answers_for_questions'][question.question_text] =\
            question.correct_answer

        context={'form': form}
        return render(request,context=context,template_name='quizyapp/quiz_question.html')

    else:
        provided_answers= request.POST
        correct_answers = request.session['correct_answers_for_questions']
        points = 0
        for question in provided_answers.keys():
            if question in correct_answers:
                if provided_answers[question] == correct_answers[question]:
                    points += 1


        #user_points = UserPoints.objects.get(user=request.user)
        user_points, created = UserPoints.objects.get_or_create(
        user=request.user,
        defaults={'points': 0})
        user_points.points += points
        user_points.save()


        context={'provided_answers':provided_answers, 'correct_answers':correct_answers, 'points':points, 'total_points':user_points.points}
        return render(request,context=context,template_name='quizyapp/correct_answers.html')

@login_required
def quiz_params(request):
    if request.method == 'GET':
        form=QuizParamsForm()
        return render(request,context={'form':form},template_name='quizyapp/quiz_params.html')

    elif request.method == 'POST':
        form=QuizParamsForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            category = form.cleaned_data['category']
            difficulty = form.cleaned_data['difficulty']

            return HttpResponseRedirect(f'/quiz/?amount={amount}&category={category}&difficulty={difficulty}')

#@login_required
class UserPointsView(ListView):
    model = UserPoints
    template_name = 'quizyapp/ranking.html'