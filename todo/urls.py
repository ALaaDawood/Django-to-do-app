from django import urls
from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("add/", views.task_view, name="add_task"),
    path("<int:task_id>/", views.task_view, name="get_update_task"),
]
