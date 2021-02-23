from django.shortcuts import render
from .forms import MultipleQuestionsForm, QuizParamsForm
from .question import QuestionList
from django.contrib.auth.decorators import login_required
from .models import UserPoints
from django.views.generic import ListView
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserPointsSerializer, UserSerializer
from django.http import HttpResponseBadRequest

@login_required
def quiz_params(request):
    if request.method == 'GET':
        form=QuizParamsForm()
        return render(request,context={'form':form},template_name='quizyapp/quiz_params.html')
    else:
        return HttpResponseBadRequest()

@login_required
def quiz_questions(request):
    if request.method == 'GET':
        params_form=QuizParamsForm(request.GET)
        if params_form.is_valid():
            amount = params_form.cleaned_data['amount']
            category = params_form.cleaned_data['category']
            difficulty = params_form.cleaned_data['difficulty']
        else:
            return HttpResponseBadRequest('Cannot generate quiz with provided parameters')

        question_list = QuestionList.fromopentdbapi(amount=amount, category=category, difficulty=difficulty)
        question_list.shuffle_answers()
        questions_form = MultipleQuestionsForm(question_list)

        request.session['correct_answers_for_questions'] = {}

        for question in question_list:
            request.session['correct_answers_for_questions'][question.question_text] =\
            question.correct_answer

        context={'form': questions_form}
        return render(request,context=context,template_name='quizyapp/quiz_questions.html')
    else:
        return HttpResponseBadRequest()

@login_required
def quiz_results(request):
    if request.method == 'POST':
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
        return render(request,context=context,template_name='quizyapp/quiz_results.html')
    else:
        return HttpResponseBadRequest()

class UserPointsView(ListView):
    model = UserPoints
    ordering = ('-points')
    template_name = 'quizyapp/ranking.html'


class UserPointsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint to display ranking
    """
    queryset = UserPoints.objects.all()
    serializer_class = model = UserPointsSerializer
    permission_classes = [permissions.AllowAny]

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

def home(request):
    return render(request, template_name='home.html')