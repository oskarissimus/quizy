from .views import quiz, quiz_params
from django.urls import path

urlpatterns = [
    path("quiz/", quiz, name="quiz"),
    path("quiz/params/", quiz_params, name="quiz_params"),
]