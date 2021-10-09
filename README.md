# Django-todo
A simple todo app built with django

### Setup
clone this repo using the following command
```bash
$ git clone https://github.com/ALaaDawood/Django-to-do-app.git
```
You will need django to be installed in you computer to run this app. Head over to https://docs.djangoproject.com/en/3.2/topics/install/for for the complete installation guide.

once installation is done, run the following command:

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

This will create and apply all the migrations file required to run the app.

last step is to run the server, using the following command

```bash
$ python manage.py runserver
```

Once the server is hosted, head over to http://127.0.0.1:8000/todolist for the App.
