from django import urls
from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("create", views.create, name="create_task"),
]
