
from django.conf.urls import include, url
from django.urls import path, reverse
from .views import dashboard, register
from django.views.generic import RedirectView


urlpatterns = [
    url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r"^register/", register, name="register"),
    path('dashboard/', dashboard, name="dashboard"),
    path('', RedirectView.as_view(url='dashboard/', permanent=False) ),
]