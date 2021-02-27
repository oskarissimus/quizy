# quizy

https://realpython.com/django-user-management/#set-up-a-django-project

## setup
```
django-admin startproject quizysite
cd quizysite
python manage.py startapp users
python manage.py migrate
python manage.py createsuperuser
```
## running
```
python manage.py runserver
http://localhost:8000/dashboard/
```

## some links
https://help.heroku.com/GDQ74SU2/django-migrations

## coverage
```
coverage run manage.py test
coverage report
coverage html
```