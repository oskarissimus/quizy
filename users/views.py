from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .forms import CustomUserCreationForm


@login_required
def dashboard(request):
    return render(request, "users/dashboard.html")


@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect(reverse("dashboard"))
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
            return redirect(reverse("register"))

