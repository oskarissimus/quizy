from django.contrib.auth import login
from django.http.response import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, "users/dashboard.html")


def register(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseBadRequest('cannot register while being logged in')
        else:
            return render(
                request, "users/register.html",
                {"form": CustomUserCreationForm}
            )
            
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("dashboard"))
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()
