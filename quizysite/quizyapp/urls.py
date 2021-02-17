from quizyapp.views import quiz
from django.conf.urls import url

urlpatterns = [
    url(r"^quiz/", quiz, name="quiz"),
]