from django.http.response import JsonResponse
from django.shortcuts import render
from django.shortcuts import HttpResponse
import urllib.request
import json
import random
from .forms import QuestionForm
# Create your views here.
def quiz(request):
    if request.method == 'GET':
        with urllib.request.urlopen('https://opentdb.com/api.php?amount=10&category=9&difficulty=easy') as response:
            json_quiz = json.load(response)
            id = 1
            for question in json_quiz['results']:
                question['id'] = id
                id+=1
                answers = [question['correct_answer']]
                answers += question['incorrect_answers']
                random.shuffle( answers )
                question['shuffled_answers'] = answers
            if 'correct_answers_for_questions' not in request.session.keys():
                request.session['correct_answers_for_questions'] = {}

            for question in json_quiz['results']:
                request.session['correct_answers_for_questions'][question['question']] =\
                question['correct_answer']

            #print (request.session['correct_answers_for_questions'])
            question = json_quiz['results'][0]['question']
            answers_in_choice_field_format =\
                [({question:answer},answer) for answer in json_quiz['results'][0]['shuffled_answers']]
            print(answers_in_choice_field_format)
            form = QuestionForm(choices=answers_in_choice_field_format, label=question)
            context={'questions': json_quiz['results'], 'form': form}
        return render(request,context=context,template_name='quizyapp/quiz_question.html')

    else:
        print(request.POST)
        return HttpResponse(f"udzielono odpowiedzi {request.POST['answers_field']}")