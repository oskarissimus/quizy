from django.shortcuts import render
from django.shortcuts import HttpResponse
# Create your views here.
def quiz(request):
    return HttpResponse("tu bedzie quiz")