from hashlib import md5
from html import unescape
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.related import ForeignKey


class Category(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    name = models.TextField(unique=True)

    def __str__(self):
        return f'id: {self.id}, name: {self.name}'


class Question(models.Model):
    id = models.CharField(max_length=32, unique=True, primary_key=True)
    text = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    Difficulty = models.TextChoices('Difficulty', 'easy medium hard')
    difficulty = models.TextField(choices=Difficulty.choices)

    def save(self, **kwargs):
        self.id = md5(''.join([self.text, self.category.name, self.difficulty]).encode(
            'utf-8')).hexdigest()
        super().save(**kwargs)

    @classmethod
    def fromopentdbformat(cls, raw_question, category):
        text = unescape(raw_question['question'])
        difficulty = raw_question['difficulty']
        return cls(text=text, category=category, difficulty=difficulty)


class Answer(models.Model):
    class Meta:
        unique_together = ['question','text']
    text = models.TextField()
    is_correct = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.PROTECT)

    def __str__(self):
        return f'text: {self.text}, is_correct: {self.is_correct}'


class UserAnswer(models.Model):
    user = ForeignKey(User, on_delete=models.PROTECT)
    question = ForeignKey(Question, on_delete=models.PROTECT)
    answer = ForeignKey(Answer, on_delete=models.PROTECT)
    date_time = models.DateTimeField(auto_now_add=True, blank=True)

    @staticmethod
    def get_points_for_user(user):
        return UserAnswer.objects.filter(user=user, answer__is_correct=True).count()

    @staticmethod
    def get_all_answers_no_for_user(user):
        return UserAnswer.objects.filter(user=user).count()

    def __str__(self):
        return f'user: {self.user.username}, question: {self.question.text}, answer: {self.answer.text}, date_time: {self.date_time}'
