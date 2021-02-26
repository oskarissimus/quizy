from .views import UserPointsViewSet, UserViewSet, home, quiz_questions, quiz_params, quiz_results, user_points
from django.urls import path
from django.urls import include, path
from rest_framework import routers


router = routers.DefaultRouter()
router.register('ranking', UserPointsViewSet)
router.register('users', UserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path("quiz/questions/", quiz_questions, name="quiz_quesions"),
    path("quiz/params/", quiz_params, name="quiz_params"),
    path("quiz/results/", quiz_results, name="quiz_results"),
    path("ranking/", user_points ,name="ranking"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', home, name='home') ,

]