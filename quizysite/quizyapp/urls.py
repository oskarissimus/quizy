from .views import quiz
from django.urls import path

urlpatterns = [
    path("quiz/", quiz, name="quiz"),
]