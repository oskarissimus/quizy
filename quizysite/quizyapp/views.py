from django.shortcuts import render
from django.shortcuts import HttpResponse
from .forms import MultipleQuestionsForm, QuestionForm
from .question import Question, QuestionList

# Create your views here.
def quiz(request):
    if request.method == 'GET':
        
        question_list = QuestionList.fromopentdbapi(amount=3, category=9, difficulty='easy')
        form = MultipleQuestionsForm(question_list)

        skip = True
        if 'correct_answers_for_questions' not in request.session.keys() or skip:
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
        return HttpResponse(f"you scored {points} pts")