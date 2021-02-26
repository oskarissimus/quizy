from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .forms import MultipleQuestionsForm, QuizParamsForm
from .models import Answer, Question, UserAnswer, Category
from .question import QuestionList
from .serializers import RankingSerializer
from .tables import UserAnswerTable


@login_required
@require_GET
def quiz_params(request):
    choices = [(c.id,c.name) for c in Category.objects.all()]
    form = QuizParamsForm(choices)
    return render(request, context={'form': form}, template_name='quizyapp/quiz_params.html')


@login_required
@require_GET
def quiz_questions(request):
    choices = [(c.id,c.name) for c in Category.objects.all()]
    params_form = QuizParamsForm(choices, request.GET)
    if params_form.is_valid():
        amount = params_form.cleaned_data['amount']
        category = params_form.cleaned_data['category']
        difficulty = params_form.cleaned_data['difficulty']
    else:
        return HttpResponseBadRequest('Cannot generate quiz with provided parameters')

    raw_question_list = QuestionList.get_raw_question_list_from_opentdb_api(
        amount=amount, category=category, difficulty=difficulty)
    question_id_list = []
    for question in raw_question_list:
        question_id_list.append(Question.fromopentdbapiformat(question).id)
    questions_form = MultipleQuestionsForm(question_id_list=question_id_list)

    request.session['question_id_list'] = question_id_list

    context = {'form': questions_form}
    return render(request, context=context, template_name='quizyapp/quiz_questions.html')


@login_required
@require_POST
def quiz_results(request):
    question_id_list = request.session['question_id_list']
    received_form = MultipleQuestionsForm(question_id_list, request.POST)

    provided_answers = {}
    correct_answers = {}
    quiz_summary = []
    points = 0
    if received_form.is_valid():
        for question_id, answer_id in received_form.cleaned_data.items():
            answer = Answer.objects.get(id=answer_id)
            if answer.is_correct:
                points += 1
            question = Question.objects.get(id=question_id)
            quiz_summary.append({
                'question': question.text,
                'provided_answer': answer.text,
                'correct_answer': question.answers.get(is_correct=True).text,
                'is_correct': answer.is_correct
            })
            UserAnswer.objects.create(
                user=request.user, question=question, answer=answer)
    else:
        return HttpResponseBadRequest()
    total_points = UserAnswer.get_points_for_user(request.user)
    context = {
        'provided_answers': provided_answers,
        'correct_answers': correct_answers,
        'points': points,
        'total_points': total_points,
        'quiz_summary': quiz_summary
    }
    return render(request, context=context, template_name='quizyapp/quiz_results.html')


@require_GET
def ranking(request):
    queryset = UserAnswer.objects.filter(answer__is_correct=True).values(
        'user__username').annotate(points=Count('user__username')).order_by('-points')
    table = UserAnswerTable(queryset)

    return render(request, 'quizyapp/ranking.html', {"table": table})


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def api_ranking(request):
    #    return Response({"message": "Hello, world!"})
    queryset = UserAnswer.objects.filter(answer__is_correct=True).values(
        'user__username').annotate(points=Count('user__username')).order_by('-points')
    serializer = RankingSerializer(queryset, many=True)
    return Response(serializer.data)


def home(request):
    return render(request, template_name='home.html')
