from django.db import models
from django.contrib.auth.models import User
from hashlib import md5
from html import unescape
from django.db.models.fields.related import ForeignKey
from .category import CategoryDict

# Create your models here.

class UserPoints(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT) 
    points = models.IntegerField()

class Category(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    name = models.TextField(unique=True)

    @classmethod
    def get_or_init_category_list_from_api(cls, category_name):

        if not Category.objects.filter(name=category_name).count():
            category_dict = CategoryDict.fromopentdbapi()
            for id, name in category_dict.items():
                Category.objects.create(id=id, name=name)

        return Category.objects.get(name=category_name)

    def __str__(self):
        return f'id: {self.id}, name: {self.name}'

class Answer(models.Model):
    id = models.CharField(max_length=32, unique=True, primary_key=True)
    text = models.TextField()
    is_correct = models.BooleanField()

    def save(self, **kwargs):
        self.id = md5(''.join([self.text, str(self.is_correct)]).encode('utf-8')).hexdigest()
        super().save(**kwargs)

    def __str__(self):
        return f'id: {self.id}, text: {self.text}, is_correct: {self.is_correct}'

class Question(models.Model):
    id = models.CharField(max_length=32, unique=True, primary_key=True)
    answers = models.ManyToManyField(Answer)
    text = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    Difficulty = models.TextChoices('Difficulty','easy medium hard')
    difficulty = models.TextField(choices=Difficulty.choices)

    def save(self, **kwargs):
        self.id = md5(''.join([self.text, self.category.name, self.difficulty]).encode('utf-8')).hexdigest()
        super().save(**kwargs)

    @classmethod
    def fromopentdbapiformat(cls, question_json):

        category = Category.get_or_init_category_list_from_api(category_name=question_json['category'])

        correct_answer = Answer(text=unescape(question_json['correct_answer']), is_correct=True)
        correct_answer.save()
        incorrect_answers = []
        for incorrect_answer_text in question_json['incorrect_answers']:
            incorrect_answer = Answer(text=unescape(incorrect_answer_text), is_correct=False)
            incorrect_answer.save()
            incorrect_answers.append(incorrect_answer)

        c = cls(
            text = unescape(question_json['question']),
            category = category,
            difficulty = question_json['difficulty']
        )
        c.save()
        c.answers.add(correct_answer, *incorrect_answers)
        return c

    def get_answers_as_choice_field_choices(self):
        return [(a.id,a.text) for a in self.answers.all()]

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
