from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserPoints(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT) 
    points = models.IntegerField()

class Category(models.Model):
    name = models.TextField(unique=True)

class Answer(models.Model):
    class Meta:
        unique_together = [('text', 'is_correct')]
    text = models.TextField()
    is_correct = models.BooleanField()

class Question(models.Model):
    answers = models.ManyToManyField(Answer)
    text = models.TextField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)



    Difficulty = models.TextChoices('Difficulty','easy medium hard')
    difficulty = models.TextField(choices=Difficulty.choices)