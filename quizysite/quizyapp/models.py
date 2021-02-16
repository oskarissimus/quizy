from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    quiz_json = models.JSONField()
    points = models.IntegerField()


