from .views import quiz, quiz_params, UserPointsView
from django.urls import path

urlpatterns = [
    path("quiz/", quiz, name="quiz"),
    path("quiz/params/", quiz_params, name="quiz_params"),
    path("ranking/", UserPointsView.as_view(),name="ranking")
]