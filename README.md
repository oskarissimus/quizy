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

## Securing

1. Generate new key with:
    ```python
    from django.core.management.utils import get_random_secret_key  
    get_random_secret_key()
    ``` 
    and paste it to `.env` file
    ```
    SECRET_KEY='your key here'
    ```
2. Add `.env` to `.gitignore` - You dont want to publish it - its yours dev secret key

3. Replace `SECRET_KEY` constant in `settings.py` with:
    ```python
    from django.core.management.utils import get_random_secret_key  
    import dotenv

    dotenv_file = os.path.join(BASE_DIR, ".env")
    if os.path.isfile(dotenv_file):
        dotenv.load_dotenv(dotenv_file)

    if 'SECRET_KEY' in os.environ:
        SECRET_KEY = os.environ['SECRET_KEY']
    else:
        SECRET_KEY = get_random_secret_key()
    ```
    This tells django to get `SECRET_KEY` from env variables. If that env variable is missing, fresh key will be generated automatically - it is useful for example in travis builds, when you dont care about env too much.

4. Set aproppriate env variable in prod env. Example for heroku:
    ```
    heroku config:set SECRET_KEY='Your secret key'
    ```
https://stackoverflow.com/questions/41298963/is-there-a-function-for-generating-settings-secret-key-in-django
## Some links
https://help.heroku.com/GDQ74SU2/django-migrations