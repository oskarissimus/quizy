# Quizy

https://realpython.com/django-user-management/#set-up-a-django-project

## Setup
```
django-admin startproject quizysite
cd quizysite
python manage.py startapp users
python manage.py migrate
python manage.py createsuperuser
```

## Running
```
python manage.py runserver
http://localhost:8000/dashboard/
```

## Testing
```
python manage.py test
```

## Coverage
```
coverage run manage.py test
coverage report
coverage html
```

## Creating fixtures
https://docs.djangoproject.com/en/3.1/howto/initial-data/
```
pip install pyyaml
python manage.py dumpdata --format=yaml -o quizyapp/fixtures/question.yaml quizyapp.question
python manage.py dumpdata --format=yaml -o quizyapp/fixtures/answer.yaml quizyapp.answer
python manage.py dumpdata --format=yaml -o quizyapp/fixtures/category.yaml quizyapp.category
python manage.py dumpdata --format=yaml -o quizyapp/fixtures/useranswer.yaml quizyapp.useranswer
python manage.py dumpdata --format=yaml -o quizyapp/fixtures/user.yaml auth.user
```

## Some links
https://help.heroku.com/GDQ74SU2/django-migrations