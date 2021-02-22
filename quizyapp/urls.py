from .views import quiz, quiz_params, UserPointsView, UserPointsViewSet,UserViewSet, home
from django.urls import path
from django.urls import include, path
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'ranking', UserPointsViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path("quiz/", quiz, name="quiz"),
    path("quiz/params/", quiz_params, name="quiz_params"),
    path("ranking/", UserPointsView.as_view(),name="ranking"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', home, name='home') ,

]