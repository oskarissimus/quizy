from .views import home, quiz_questions, quiz_params, quiz_results, ranking, api_ranking
from django.urls import path
from django.urls import include, path

urlpatterns = [
    path('api/ranking/', api_ranking, name="api_ranking"),
    path("quiz/questions/", quiz_questions, name="quiz_quesions"),
    path("quiz/params/", quiz_params, name="quiz_params"),
    path("quiz/results/", quiz_results, name="quiz_results"),
    path("ranking/", ranking ,name="ranking"),
    path('', home, name='home') ,

]